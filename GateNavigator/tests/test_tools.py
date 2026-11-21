import pytest

from app.tools import gate_marks_calculator


def test_marks_calculation():
    result = gate_marks_calculator(
        mcq_1_correct=5,
        mcq_1_wrong=3,
        mcq_2_correct=4,
        mcq_2_wrong=2,
        msq_correct=3,
        msq_wrong=1,
        nat_correct=5,
        nat_wrong=2,
    )

    assert result["correct_marks"] == 29
    assert result["marks_lost_to_negatives"] == pytest.approx(2.33)
    assert result["total_marks"] == pytest.approx(26.67)


def test_no_negative_marks_for_msq_and_nat():
    result = gate_marks_calculator(
        mcq_1_correct=0,
        mcq_1_wrong=0,
        mcq_2_correct=0,
        mcq_2_wrong=0,
        msq_correct=2,
        msq_wrong=3,
        nat_correct=2,
        nat_wrong=3,
    )

    assert result["correct_marks"] == 8
    assert result["marks_lost_to_negatives"] == 0
    assert result["total_marks"] == 8


def test_total_marks_never_below_zero():
    result = gate_marks_calculator(
        mcq_1_correct=0,
        mcq_1_wrong=100,
        mcq_2_correct=0,
        mcq_2_wrong=0,
        msq_correct=0,
        msq_wrong=0,
        nat_correct=0,
        nat_wrong=0,
    )

    assert result["total_marks"] == 0


def test_negative_input_raises_error():
    with pytest.raises(ValueError):
        gate_marks_calculator(
            mcq_1_correct=-1,
            mcq_1_wrong=0,
            mcq_2_correct=0,
            mcq_2_wrong=0,
            msq_correct=0,
            msq_wrong=0,
            nat_correct=0,
            nat_wrong=0,
        )


def test_boolean_input_raises_error():
    with pytest.raises(ValueError):
        gate_marks_calculator(
            mcq_1_correct=True,
            mcq_1_wrong=0,
            mcq_2_correct=0,
            mcq_2_wrong=0,
            msq_correct=0,
            msq_wrong=0,
            nat_correct=0,
            nat_wrong=0,
        )
