
import json
import os
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st

# --------------------------------
# 1. Page Configuration
# --------------------------------

st.set_page_config(page_title="GATENavigator", page_icon="🎓", layout="centered")

st.title("🎓 GATENavigator")
st.caption("Your AI-powered GATE preparation assistant")

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

FEEDBACK_FILE = Path(__file__).resolve().parent.parent / "Data" / "feedback.json"

# Create feedback file if it doesn't exist
FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

if not FEEDBACK_FILE.exists():
    FEEDBACK_FILE.write_text("[]", encoding="utf-8")


# --------------------------------
# 2. Feedback Function
# --------------------------------


def save_feedback(question, answer, feedback):

    try:
        feedback_data = json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))

        if not isinstance(feedback_data, list):
            feedback_data = []

    except (json.JSONDecodeError, OSError):
        feedback_data = []

    new_feedback = {
        "question": question,
        "answer": answer,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat(),
    }

    feedback_data.append(new_feedback)

    FEEDBACK_FILE.write_text(json.dumps(feedback_data, indent=4), encoding="utf-8")


# --------------------------------
# 3. Session State
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit-student-1"

if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = False


# --------------------------------
# 4. Chat Mode Selection
# --------------------------------

mode = st.radio("Choose Chat Mode", ["RAG Mode", "Agent Mode"], horizontal=True)


# --------------------------------
# 5. Display Chat History
# --------------------------------

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display citations
        if message.get("citations"):
            st.markdown("**Sources:**")

            for citation in message["citations"]:
                st.caption(f"{citation.get('source')} | Page: {citation.get('page')}")

        # Display feedback buttons only for assistant messages
        if message["role"] == "assistant":
            question = ""

            if i > 0 and st.session_state.messages[i - 1]["role"] == "user":
                question = st.session_state.messages[i - 1]["content"]

            # Avoid saving feedback multiple times for one answer
            if message.get("feedback"):
                st.caption(f"Feedback submitted: {message['feedback']}")

            else:
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("👍", key=f"up_{i}"):
                        save_feedback(question, message["content"], "positive")

                        message["feedback"] = "positive"
                        st.success("Positive feedback saved!")
                        st.rerun()

                with col2:
                    if st.button("👎", key=f"down_{i}"):
                        save_feedback(question, message["content"], "negative")

                        message["feedback"] = "negative"
                        st.success("Negative feedback saved!")
                        st.rerun()


# --------------------------------
# 6. Approval Interface
# --------------------------------

if st.session_state.pending_approval:
    st.warning("Human approval is required before marks calculation.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Approve"):
            try:
                response = requests.post(
                    f"{BASE_URL}/agent",
                    json={"thread_id": st.session_state.thread_id, "approval": True},
                    timeout=120,
                )

                response.raise_for_status()
                result = response.json()

                data = result.get("result", {}).get("data", {})

                st.session_state.messages.append(
                    {"role": "assistant", "content": str(data), "citations": []}
                )

                st.session_state.pending_approval = False
                st.rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"Approval failed: {e}")

    with col2:
        if st.button("Decline"):
            try:
                response = requests.post(
                    f"{BASE_URL}/agent",
                    json={"thread_id": st.session_state.thread_id, "approval": False},
                    timeout=120,
                )

                response.raise_for_status()
                result = response.json()

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": str(result.get("result", {})),
                        "citations": [],
                    }
                )

                st.session_state.pending_approval = False
                st.rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"Decline failed: {e}")


# --------------------------------
# 7. Chat Input
# --------------------------------

prompt = st.chat_input("Ask anything about GATE...")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"), st.spinner("Processing your question..."):
        try:
            # ----------------------------
            # RAG Mode
            # ----------------------------

            if mode == "RAG Mode":
                response = requests.post(
                    f"{BASE_URL}/ask", json={"question": prompt}, timeout=120
                )

                response.raise_for_status()
                result = response.json()

                answer = result.get("answer", "No answer received.")

                citations = result.get("citations", [])

            # ----------------------------
            # Agent Mode
            # ----------------------------

            else:
                response = requests.post(
                    f"{BASE_URL}/agent",
                    json={
                        "question": prompt,
                        "thread_id": st.session_state.thread_id,
                    },
                    timeout=120,
                )

                response.raise_for_status()
                result = response.json()

                if result.get("status") == "approval_required":
                    st.session_state.pending_approval = True

                    answer = (
                        "Your request requires human approval. "
                        "Please approve or decline above."
                    )

                    citations = []

                elif result.get("status") == "completed":
                    agent_result = result.get("result", {})
                    data = agent_result.get("data", {})

                    if agent_result.get("tool") == "rag_search":
                        answer = data.get("answer", "No answer received.")

                        citations = data.get("citations", [])

                    else:
                        answer = str(data or agent_result)
                        citations = []

                else:
                    answer = str(result)
                    citations = []

            # Display answer immediately
            st.markdown(answer)

            # Display citations
            if citations:
                st.markdown("**Sources:**")

                for citation in citations:
                    st.caption(
                        f"{citation.get('source')} | Page: {citation.get('page')}"
                    )

            # Display feedback buttons immediately
            col1, col2 = st.columns(2)

            with col1:
                if st.button("👍", key="new_up"):
                    save_feedback(prompt, answer, "positive")

                    # Update latest assistant message
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "citations": citations,
                            "feedback": "positive",
                        }
                    )

                    st.success("Positive feedback saved!")
                    st.rerun()

            with col2:
                if st.button("👎", key="new_down"):
                    save_feedback(prompt, answer, "negative")

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "citations": citations,
                            "feedback": "negative",
                        }
                    )

                    st.success("Negative feedback saved!")
                    st.rerun()

            # Save answer if no feedback button was clicked
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "citations": citations}
            )

        except requests.exceptions.RequestException as e:
            error_message = f"Backend connection failed: {e}"

            st.error(error_message)

            st.session_state.messages.append(
                {"role": "assistant", "content": error_message, "citations": []}
            )


# --------------------------------
# 8. What Changed in GATE 2027?
# --------------------------------

st.divider()

st.header("🔍 What Changed in GATE 2027?")

st.write("Compare the GATE 2026 and GATE 2027 Computer Science syllabus.")

DIFF_FILE = Path(__file__).resolve().parent.parent / "Data" / "cs_syllabus_diff.json"

try:
    with open(DIFF_FILE, "r", encoding="utf-8") as file:
        diff_data = json.load(file)

    paper_name = diff_data["paper_name"]

    st.subheader(f"📘 {paper_name}")

    # Official syllabus PDF links
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### GATE 2026")
        st.markdown(f"[📄 Open 2026 Syllabus]({diff_data['year_2026']['pdf']})")

    with col2:
        st.markdown("### GATE 2027")
        st.markdown(f"[📄 Open 2027 Syllabus]({diff_data['year_2027']['pdf']})")

    st.divider()

    # Display section-wise comparison
    for section in diff_data["sections"]:
        section_name = section["name"]

        # Page numbers verified from both PDFs
        page = 2 if "network" in section_name.lower() else 1

        with st.expander(section_name, expanded=False):
            left, right = st.columns(2)

            # Added topics
            with left:
                st.markdown("### 🟢 Added in 2027")

                if section["added"]:
                    for topic in section["added"]:
                        st.markdown(f"- {topic}")

                        st.caption(
                            f"[View 2027 PDF — Page {page}]"
                            f"({diff_data['year_2027']['pdf']}#page={page})"
                        )

                else:
                    st.write("No additions identified.")

            # Removed topics
            with right:
                st.markdown("### 🔴 Removed / Not explicitly listed")

                if section["removed"]:
                    for topic in section["removed"]:
                        st.markdown(f"- {topic}")

                        st.caption(
                            f"[View 2026 PDF — Page {page}]"
                            f"({diff_data['year_2026']['pdf']}#page={page})"
                        )

                else:
                    st.write("No removals identified.")

            # Unchanged section
            if section["status"] == "unchanged":
                st.success("No wording changes identified.")

    st.divider()

    st.info(
        "Note: A topic not explicitly listed in the 2027 "
        "syllabus is not necessarily officially removed. "
        "Always refer to the official syllabus."
    )

except FileNotFoundError:
    st.error(
        "Syllabus comparison JSON file not found. Check Data/cs_syllabus_diff.json."
    )

except (json.JSONDecodeError, KeyError) as e:
    st.error(f"Could not load syllabus comparison: {e}")
