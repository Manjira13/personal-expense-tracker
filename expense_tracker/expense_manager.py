"""Business logic for managing transactions and producing summaries."""

import sqlite3
from datetime import date
from decimal import Decimal
from typing import List, Optional

from .database import get_connection
from .models import (
    Transaction,
    amount_to_paise,
    paise_to_amount
)


class ExpenseManager:
    """Provides CRUD, filtering, and summary operations."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    @staticmethod
    def _row_to_transaction(
        row: sqlite3.Row
    ) -> Transaction:

        return Transaction(
            transaction_id=row["id"],
            title=row["title"],
            amount=paise_to_amount(row["amount_paise"]),
            transaction_type=row["transaction_type"],
            category=row["category"],
            transaction_date=date.fromisoformat(
                row["transaction_date"]
            ),
            notes=row["notes"],
        )

    def add_transaction(
        self,
        transaction: Transaction
    ) -> int:

        with get_connection(self.db_path) as connection:

            cursor = connection.execute(
                """
                INSERT INTO transactions
                (
                    title,
                    amount_paise,
                    transaction_type,
                    category,
                    transaction_date,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction.title,
                    amount_to_paise(transaction.amount),
                    transaction.transaction_type,
                    transaction.category,
                    transaction.transaction_date.isoformat(),
                    transaction.notes
                )
            )

            return int(cursor.lastrowid)

    def get_all_transactions(self) -> List[Transaction]:

        with get_connection(self.db_path) as connection:

            rows = connection.execute(
                """
                SELECT *
                FROM transactions
                ORDER BY transaction_date DESC, id DESC
                """
            ).fetchall()

        return [
            self._row_to_transaction(row)
            for row in rows
        ]

    def get_transaction(
        self,
        transaction_id: int
    ) -> Optional[Transaction]:

        with get_connection(self.db_path) as connection:

            row = connection.execute(
                """
                SELECT *
                FROM transactions
                WHERE id = ?
                """,
                (transaction_id,)
            ).fetchone()

        return (
            self._row_to_transaction(row)
            if row else None
        )

    def update_transaction(
        self,
        transaction_id: int,
        transaction: Transaction
    ) -> bool:

        with get_connection(self.db_path) as connection:

            cursor = connection.execute(
                """
                UPDATE transactions
                SET
                    title = ?,
                    amount_paise = ?,
                    transaction_type = ?,
                    category = ?,
                    transaction_date = ?,
                    notes = ?
                WHERE id = ?
                """,
                (
                    transaction.title,
                    amount_to_paise(transaction.amount),
                    transaction.transaction_type,
                    transaction.category,
                    transaction.transaction_date.isoformat(),
                    transaction.notes,
                    transaction_id
                )
            )

            return cursor.rowcount > 0

    def delete_transaction(
        self,
        transaction_id: int
    ) -> bool:

        with get_connection(self.db_path) as connection:

            cursor = connection.execute(
                """
                DELETE FROM transactions
                WHERE id = ?
                """,
                (transaction_id,)
            )

            return cursor.rowcount > 0

    def filter_transactions(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category: Optional[str] = None,
        transaction_type: Optional[str] = None,
    ) -> List[Transaction]:

        clauses = []
        params = []

        if start_date:
            clauses.append(
                "transaction_date >= ?"
            )
            params.append(start_date.isoformat())

        if end_date:
            clauses.append(
                "transaction_date <= ?"
            )
            params.append(end_date.isoformat())

        if category:
            clauses.append(
                "LOWER(category) = LOWER(?)"
            )
            params.append(category.strip())

        if transaction_type:

            normalized_type = (
                transaction_type.strip().lower()
            )

            if normalized_type not in {"income", "expense"}:
                raise ValueError(
                    "Transaction type must be 'income' or 'expense'."
                )

            clauses.append(
                "transaction_type = ?"
            )

            params.append(normalized_type)

        query = "SELECT * FROM transactions"

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        query += (
            " ORDER BY transaction_date DESC, id DESC"
        )

        with get_connection(self.db_path) as connection:

            rows = connection.execute(
                query,
                params
            ).fetchall()

        return [
            self._row_to_transaction(row)
            for row in rows
        ]

    def monthly_summary(
        self,
        year: int,
        month: int
    ) -> dict:

        if not 1 <= month <= 12:
            raise ValueError(
                "Month must be between 1 and 12."
            )

        month_key = f"{year:04d}-{month:02d}"

        with get_connection(self.db_path) as connection:

            rows = connection.execute(
                """
                SELECT
                    transaction_type,
                    SUM(amount_paise) AS total
                FROM transactions
                WHERE substr(transaction_date, 1, 7) = ?
                GROUP BY transaction_type
                """,
                (month_key,)
            ).fetchall()

        totals = {
            "income": 0,
            "expense": 0
        }

        for row in rows:
            totals[row["transaction_type"]] = (
                row["total"] or 0
            )

        income = paise_to_amount(
            totals["income"]
        )

        expenses = paise_to_amount(
            totals["expense"]
        )

        return {
            "year": year,
            "month": month,
            "income": income,
            "expenses": expenses,
            "balance": income - expenses
        }

    def overall_summary(self) -> dict:

        with get_connection(self.db_path) as connection:

            rows = connection.execute(
                """
                SELECT
                    transaction_type,
                    SUM(amount_paise) AS total
                FROM transactions
                GROUP BY transaction_type
                """
            ).fetchall()

        totals = {
            "income": 0,
            "expense": 0
        }

        for row in rows:
            totals[row["transaction_type"]] = (
                row["total"] or 0
            )

        income = paise_to_amount(
            totals["income"]
        )

        expenses = paise_to_amount(
            totals["expense"]
        )

        return {
            "income": income,
            "expenses": expenses,
            "balance": income - expenses
        }
