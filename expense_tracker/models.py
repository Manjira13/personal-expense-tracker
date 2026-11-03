"""Transaction model and input validation."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional


VALID_TYPES = {"income", "expense"}

DEFAULT_CATEGORIES = {
    "income": [
        "Salary",
        "Freelance",
        "Investment",
        "Gift",
        "Other"
    ],
    "expense": [
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Education",
        "Health",
        "Entertainment",
        "Other"
    ],
}


def amount_to_paise(value: object) -> int:
    """Convert a positive amount to integer paise."""

    try:
        amount = Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

    except (InvalidOperation, ValueError):
        raise ValueError(
            "Amount must be a valid number."
        ) from None

    if not amount.is_finite() or amount <= 0:
        raise ValueError(
            "Amount must be greater than zero."
        )

    return int(amount * 100)


def paise_to_amount(paise: int) -> Decimal:
    """Convert integer paise to a Decimal amount in rupees."""

    return (
        Decimal(paise) / Decimal(100)
    ).quantize(Decimal("0.01"))


@dataclass
class Transaction:
    title: str
    amount: Decimal
    transaction_type: str
    category: str
    transaction_date: date
    notes: str = ""
    transaction_id: Optional[int] = None

    def __post_init__(self) -> None:

        self.title = self.title.strip()
        self.category = self.category.strip()
        self.notes = self.notes.strip()

        self.transaction_type = (
            self.transaction_type.strip().lower()
        )

        if not self.title:
            raise ValueError(
                "Title cannot be empty."
            )

        if self.transaction_type not in VALID_TYPES:
            raise ValueError(
                "Transaction type must be 'income' or 'expense'."
            )

        if not self.category:
            raise ValueError(
                "Category cannot be empty."
            )

        if not isinstance(self.transaction_date, date):
            raise ValueError(
                "Transaction date must be a date."
            )

        self.amount = paise_to_amount(
            amount_to_paise(self.amount)
        )
