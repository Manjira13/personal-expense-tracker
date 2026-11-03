"""SQLite database setup and low-level data access."""

import sqlite3
from pathlib import Path
from typing import Optional


DEFAULT_DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "expenses.db"
)


def get_connection(
    db_path: Optional[str] = None
) -> sqlite3.Connection:
    """Open a SQLite connection."""

    path = Path(db_path) if db_path else DEFAULT_DB_PATH

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(path)

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def initialize_database(
    db_path: Optional[str] = None
) -> None:
    """Create the transactions table if it does not exist."""

    with get_connection(db_path) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL
                    CHECK(length(trim(title)) > 0),

                amount_paise INTEGER NOT NULL
                    CHECK(amount_paise > 0),

                transaction_type TEXT NOT NULL
                    CHECK(transaction_type IN ('income', 'expense')),

                category TEXT NOT NULL
                    CHECK(length(trim(category)) > 0),

                transaction_date TEXT NOT NULL,

                notes TEXT NOT NULL DEFAULT ''
            )
        """)
