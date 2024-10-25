import pytest

from services.npi_service import evaluate_rpn


def test_evaluate_rpn_addition():
    assert evaluate_rpn("3 4 +") == 7.0


def test_evaluate_rpn_subtraction():
    assert evaluate_rpn("10 3 -") == 7.0


def test_evaluate_rpn_multiplication():
    assert evaluate_rpn("5 6 *") == 30.0


def test_evaluate_rpn_division():
    assert evaluate_rpn("8 2 /") == 4.0


def test_evaluate_rpn_complex_expression():
    assert evaluate_rpn("3 5 + 2 *") == 16.0


def test_evaluate_rpn_division_by_zero():
    with pytest.raises(ValueError, match="Error: division by zero"):
        evaluate_rpn("4 0 /")


def test_evaluate_rpn_invalid_expression():
    with pytest.raises(ValueError, match="Error: invalid RPN expression"):
        evaluate_rpn("3 +")


def test_evaluate_rpn_negative_numbers():
    assert evaluate_rpn("-1 1 +") == 0.0
    assert evaluate_rpn("-1 -1 +") == -2.0


def test_evaluate_rpn_float_numbers():
    assert evaluate_rpn("3.5 4.5 +") == 8.0
    assert evaluate_rpn("5.0 2.0 /") == 2.5


def test_evaluate_rpn_multiple_operations():
    assert evaluate_rpn("2 3 + 4 *") == 20.0
    assert evaluate_rpn("10 2 5 * +") == 20.0


def test_evaluate_rpn_spaces():
    assert evaluate_rpn("  3   4  +  ") == 7.0


def test_evaluate_rpn_too_few_operands():
    with pytest.raises(ValueError, match="Error: invalid RPN expression"):
        evaluate_rpn("3 + 5")
