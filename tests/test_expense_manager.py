from datetime import date
from decimal import Decimal

import pytest

from expense_tracker.database import initialize_database
from expense_tracker.expense_manager import ExpenseManager
from expense_tracker.models import Transaction


def make_transaction(
    title,
    amount,
    kind="expense",
    category="Food",
    day=date(2026, 3, 10)
):

    return Transaction(
        title,
        Decimal(str(amount)),
        kind,
        category,
        day
    )


def setup_manager(tmp_path):

    db_path = str(tmp_path / "test.db")

    initialize_database(db_path)

    return ExpenseManager(db_path)


def test_add_get_update_delete_transaction(tmp_path):

    manager = setup_manager(tmp_path)

    transaction_id = manager.add_transaction(
        make_transaction("Lunch", "120")
    )

    saved = manager.get_transaction(transaction_id)

    assert saved.title == "Lunch"

    assert saved.amount == Decimal("120.00")

    updated = make_transaction("Dinner", "250")

    assert manager.update_transaction(
        transaction_id,
        updated
    ) is True

    assert manager.get_transaction(
        transaction_id
    ).title == "Dinner"

    assert manager.delete_transaction(
        transaction_id
    ) is True

    assert manager.get_transaction(
        transaction_id
    ) is None

    assert manager.delete_transaction(
        transaction_id
    ) is False


def test_filter_by_category_and_type(tmp_path):

    manager = setup_manager(tmp_path)

    manager.add_transaction(
        make_transaction(
            "Lunch", "100", "expense", "Food"
        )
    )

    manager.add_transaction(
        make_transaction(
            "Salary", "1000", "income", "Salary"
        )
    )

    results = manager.filter_transactions(
        category="food",
        transaction_type="expense"
    )

    assert len(results) == 1

    assert results[0].title == "Lunch"


def test_monthly_summary(tmp_path):

    manager = setup_manager(tmp_path)

    manager.add_transaction(
        make_transaction(
            "Salary",
            "2000",
            "income",
            "Salary",
            date(2026, 3, 1)
        )
    )

    manager.add_transaction(
        make_transaction(
            "Food",
            "250",
            "expense",
            "Food",
            date(2026, 3, 2)
        )
    )

    manager.add_transaction(
        make_transaction(
            "April rent",
            "500",
            "expense",
            "Bills",
            date(2026, 4, 1)
        )
    )

    summary = manager.monthly_summary(2026, 3)

    assert summary["income"] == Decimal("2000.00")

    assert summary["expenses"] == Decimal("250.00")

    assert summary["balance"] == Decimal("1750.00")


def test_invalid_month_is_rejected(tmp_path):

    manager = setup_manager(tmp_path)

    with pytest.raises(ValueError):

        manager.monthly_summary(2026, 13)
