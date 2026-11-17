
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

from app.rag import answer_question
from app.tools import gate_marks_calculator


# ---------------------------------
# 1. Define Agent State
# ---------------------------------

class AgentState(TypedDict, total=False):
    question: str
    task: str
    marks_data: dict
    approved: bool
    result: dict
    history: list


# ---------------------------------
# 2. Identify the Required Tool
# ---------------------------------

def route_request(state: AgentState):

    question = state["question"].lower()

    marks_keywords = [
        "calculate marks",
        "marks calculator",
        "calculate my score",
        "mock test marks"
    ]

    if any(keyword in question for keyword in marks_keywords):
        return {"task": "marks"}

    return {"task": "rag"}


def select_next_step(state: AgentState):

    if state["task"] == "marks":
        return "approval"

    return "rag"


# ---------------------------------
# 3. Approval Node
# ---------------------------------

def approval_node(state: AgentState):

    approval = interrupt({
        "message": "Do you approve the GATE marks calculation?",
        "action": "calculate_marks"
    })

    return {"approved": bool(approval)}


def check_approval(state: AgentState):

    if state.get("approved"):
        return "calculate"

    return "decline"


# ---------------------------------
# 4. Marks Calculator Node
# ---------------------------------

def marks_node(state: AgentState):

    result = gate_marks_calculator(**state["marks_data"])

    return {
        "result": {
            "tool": "gate_marks_calculator",
            "data": result
        }
    }


# ---------------------------------
# 5. RAG Search Node
# ---------------------------------

def rag_node(state: AgentState):

    result = answer_question(state["question"])

    return {
        "result": {
            "tool": "rag_search",
            "data": result
        }
    }


# ---------------------------------
# 6. Decline Node
# ---------------------------------

def decline_node(state: AgentState):

    return {
        "result": {
            "message": "Marks calculation was not approved."
        }
    }


# ---------------------------------
# 7. Memory Node
# ---------------------------------

def memory_node(state: AgentState):

    history = state.get("history", [])

    updated_history = history + [
        {
            "question": state["question"],
            "result": state["result"]
        }
    ]

    return {"history": updated_history}


# ---------------------------------
# 8. Build LangGraph Workflow
# ---------------------------------

workflow = StateGraph(AgentState)

workflow.add_node("route", route_request)
workflow.add_node("approval", approval_node)
workflow.add_node("calculate", marks_node)
workflow.add_node("rag", rag_node)
workflow.add_node("decline", decline_node)
workflow.add_node("memory", memory_node)

workflow.add_edge(START, "route")

workflow.add_conditional_edges(
    "route",
    select_next_step,
    {
        "approval": "approval",
        "rag": "rag"
    }
)

workflow.add_conditional_edges(
    "approval",
    check_approval,
    {
        "calculate": "calculate",
        "decline": "decline"
    }
)

workflow.add_edge("calculate", "memory")
workflow.add_edge("rag", "memory")
workflow.add_edge("decline", "memory")
workflow.add_edge("memory", END)

# Memory checkpoint
memory = MemorySaver()

# Compile graph
agent_graph = workflow.compile(checkpointer=memory)


# ---------------------------------
# 9. Run Agent
# ---------------------------------

if __name__ == "__main__":

    print("================================")
    print("    GATENavigator LangGraph")
    print("================================")

    thread_id = "gate-student-1"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    while True:

        question = input("\nAsk a question or type 'exit': ")

        if question.lower() in ["exit", "quit"]:
            break

        marks_data = {}

        if question.lower() in [
            "calculate marks",
            "marks calculator",
            "calculate my score",
            "mock test marks"
        ]:

            print("\nEnter your mock test results:")

            try:
                marks_data = {
                    "mcq_1_correct": int(input("Correct 1-mark MCQs: ")),
                    "mcq_1_wrong": int(input("Wrong 1-mark MCQs: ")),
                    "mcq_2_correct": int(input("Correct 2-mark MCQs: ")),
                    "mcq_2_wrong": int(input("Wrong 2-mark MCQs: ")),
                    "msq_correct": int(input("Correct MSQs: ")),
                    "msq_wrong": int(input("Wrong MSQs: ")),
                    "nat_correct": int(input("Correct NATs: ")),
                    "nat_wrong": int(input("Wrong NATs: "))
                }

            except ValueError:
                print("Please enter valid non-negative integers.")
                continue

        try:

            response = agent_graph.invoke(
                {
                    "question": question,
                    "marks_data": marks_data
                },
                config=config
            )

            # Handle approval request
            if "__interrupt__" in response:

                print("\nApproval Required:")
                print(response["__interrupt__"][0].value)

                approval = input(
                    "\nApprove calculation? (yes/no): "
                ).strip().lower()

                response = agent_graph.invoke(
                    Command(resume=(approval == "yes")),
                    config=config
                )

            print("\nAgent Response:")
            print(response.get("result"))

            print(
                "\nConversation history entries:",
                len(response.get("history", []))
            )

        except Exception as error:
            print("Agent Error:", error)
