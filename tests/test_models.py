from datetime import date
from decimal import Decimal

import pytest

from expense_tracker.models import (
    Transaction,
    amount_to_paise,
    paise_to_amount
)


def test_amount_conversion_avoids_float_storage():

    assert amount_to_paise("12.34") == 1234

    assert paise_to_amount(1234) == Decimal("12.34")


@pytest.mark.parametrize(
    "value",
    ["0", "-1", "abc", "NaN"]
)
def test_invalid_amount_is_rejected(value):

    with pytest.raises(ValueError):
        amount_to_paise(value)


def test_transaction_normalizes_type_and_text():

    transaction = Transaction(
        "  Lunch ",
        Decimal("50"),
        "EXPENSE",
        " Food ",
        date(2026, 1, 2)
    )

    assert transaction.title == "Lunch"
    assert transaction.category == "Food"
    assert transaction.transaction_type == "expense"


def test_empty_title_is_rejected():

    with pytest.raises(ValueError):

        Transaction(
            " ",
            Decimal("10"),
            "expense",
            "Food",
            date.today()
        )
