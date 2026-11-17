
from app.rag import answer_question
from app.tools import gate_marks_calculator


def run_agent(user_input):
    """
    Simple hand-written agent.

    It decides whether to use RAG search or
    the GATE marks calculator.
    """

    user_input = user_input.strip()

    print("\nAgent is analyzing your request...")

    # Tool 1: GATE marks calculator
    if user_input.lower() in ["calculate marks", "marks calculator"]:

        print("Agent selected: GATE Marks Calculator")

        try:
            print("\nEnter your mock test results:")

            result = gate_marks_calculator(
                mcq_1_correct=int(input("Correct 1-mark MCQs: ")),
                mcq_1_wrong=int(input("Wrong 1-mark MCQs: ")),
                mcq_2_correct=int(input("Correct 2-mark MCQs: ")),
                mcq_2_wrong=int(input("Wrong 2-mark MCQs: ")),
                msq_correct=int(input("Correct MSQs: ")),
                msq_wrong=int(input("Wrong MSQs: ")),
                nat_correct=int(input("Correct NATs: ")),
                nat_wrong=int(input("Wrong NATs: "))
            )

            return {
                "tool": "gate_marks_calculator",
                "result": result
            }

        except ValueError as error:
            return {
                "tool": "gate_marks_calculator",
                "error": str(error)
            }

    # Tool 2: RAG search
    else:

        print("Agent selected: RAG Search")

        result = answer_question(user_input)

        return {
            "tool": "rag_search",
            "result": result
        }


if __name__ == "__main__":

    print("================================")
    print("       GATENavigator Agent")
    print("================================")

    while True:

        user_input = input(
            "\nAsk a GATE question or type 'calculate marks': "
        )

        if user_input.lower() in ["exit", "quit"]:
            print("Agent stopped.")
            break

        try:
            response = run_agent(user_input)

            print("\nAgent Response:")
            print(response)

        except Exception as error:
            print("Agent Error:", error)
