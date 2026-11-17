
def gate_marks_calculator(
    mcq_1_correct,
    mcq_1_wrong,
    mcq_2_correct,
    mcq_2_wrong,
    msq_correct,
    msq_wrong,
    nat_correct,
    nat_wrong
):
    """
    Calculate GATE mock test marks using official negative marking rules.

    MCQ 1-mark wrong answer: -1/3
    MCQ 2-mark wrong answer: -2/3
    MSQ and NAT: No negative marking
    """

    values = [
        mcq_1_correct, mcq_1_wrong,
        mcq_2_correct, mcq_2_wrong,
        msq_correct, msq_wrong,
        nat_correct, nat_wrong
    ]

    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
        raise ValueError("All question counts must be non-negative integers.")

    # Marks earned from correct answers
    correct_marks = (
        mcq_1_correct * 1
        + mcq_2_correct * 2
        + msq_correct * 2
        + nat_correct * 2
    )

    # Negative marks for incorrect MCQs only
    negative_marks = (
        mcq_1_wrong * (1 / 3)
        + mcq_2_wrong * (2 / 3)
    )

    # Final score
    total_marks = correct_marks - negative_marks

    if total_marks < 0:
        total_marks = 0

    return {
        "correct_marks": round(correct_marks, 2),
        "marks_lost_to_negatives": round(negative_marks, 2),
        "total_marks": round(total_marks, 2),
        "maximum_marks": 100
    }


if __name__ == "__main__":
    result = gate_marks_calculator(
        mcq_1_correct=5,
        mcq_1_wrong=3,
        mcq_2_correct=4,
        mcq_2_wrong=2,
        msq_correct=3,
        msq_wrong=1,
        nat_correct=5,
        nat_wrong=2
    )

    print("GATE Mock Test Results")
    print("----------------------")

    for key, value in result.items():
        print(f"{key}: {value}")
