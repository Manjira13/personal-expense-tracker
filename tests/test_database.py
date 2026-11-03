import sqlite3
import pytest

from expense_tracker.database import (
    initialize_database,
    get_connection
)


def test_initialize_database_creates_transactions_table(
    tmp_path
):

    db_path = str(tmp_path / "test.db")

    initialize_database(db_path)

    with get_connection(db_path) as connection:

        row = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='transactions'
            """
        ).fetchone()

    assert row["name"] == "transactions"


def test_database_rejects_invalid_transaction_type(
    tmp_path
):

    db_path = str(tmp_path / "test.db")

    initialize_database(db_path)

    with pytest.raises(sqlite3.IntegrityError):

        with get_connection(db_path) as connection:

            connection.execute(
                """
                INSERT INTO transactions
                (
                    title,
                    amount_paise,
                    transaction_type,
                    category,
                    transaction_date
                )
                VALUES (
                    'Test',
                    100,
                    'transfer',
                    'Other',
                    '2026-01-01'
                )
                """
            )
