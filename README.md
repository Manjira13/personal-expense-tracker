# Personal Expense Tracker

A command-line personal finance application built with
Python and SQLite. It supports recording income and
expenses, managing transactions, filtering records,
and viewing financial summaries.

## Features

- Add, view, update, and delete income and expense
  transactions (CRUD).
- Categorize transactions (for example, Food, Travel,
  Shopping, Bills, Education, and Salary).
- Filter transactions by date range, category, and
  transaction type.
- View overall income, expenses, and balance.
- Generate monthly income and expense summaries.
- Persist records in a local SQLite database.
- Validate transaction details and handle common
  input errors.
- Store monetary values as integer paise in SQLite
  to avoid floating-point arithmetic errors.
- Automated tests using pytest.

## Tech Stack

- Python 3.12+
- SQLite
- Python sqlite3 standard-library module
- pytest

## Project Structure

personal-expense-tracker/
├── main.py
├── expense_tracker/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── expense_manager.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_database.py
│   └── test_expense_manager.py
├── data/
│   └── .gitkeep
├── requirements.txt
├── .gitignore
└── README.md

## Setup

### 1. Clone the repository

git clone https://github.com/YOUR-USERNAME/personal-expense-tracker.git

cd personal-expense-tracker

### 2. Create and activate a virtual environment

Windows PowerShell:

python -m venv .venv

.\.venv\Scripts\Activate.ps1

macOS/Linux:

python3 -m venv .venv

source .venv/bin/activate

### 3. Install dependencies

python -m pip install -r requirements.txt

SQLite and sqlite3 are included with standard Python
installations; no separate database server is required.

## Run the Application

From the repository root:

python main.py

The database is created automatically at
data/expenses.db the first time the application runs.

## Menu

1. Add transaction
2. View transactions
3. Update transaction
4. Delete transaction
5. Filter transactions
6. Overall summary
7. Monthly summary
0. Exit

Dates must use YYYY-MM-DD.
Amounts are entered in rupees and must be greater than zero.

## Run Tests

pytest -v

The tests cover:

- Amount conversion and validation.
- Transaction model validation.
- Database initialization and constraints.
- CRUD operations.
- Transaction filtering.
- Monthly financial summaries.

Tests use temporary databases so they do not modify
the application's real database.

## Design Notes

- Separation of concerns: the CLI, transaction model,
  business logic, and database access are kept in
  separate modules.
- Parameterized SQL: user-provided values are passed
  as SQL parameters rather than interpolated into
  query strings.
- Money representation: amounts are converted to
  integer paise for storage and Decimal for calculations
  and display.
- Persistence: SQLite stores records locally between
  application runs.
- Data privacy: the local database is excluded from Git
  by .gitignore.

## Current Limitations

- This is a single-user, local command-line application;
  it does not include authentication or cloud
  synchronization.
- Categories are free-text values rather than a
  separately managed category table.
- The application does not import bank statements,
  connect to financial institutions, or generate
  PDF reports.
- There is no graphical or web interface.

## Future Improvements

- Add category management and category-wise
  spending reports.
- Add export to CSV.
- Add configurable monthly budgets.
- Improve CLI input flows and add pagination.
- Add integration tests and broader edge-case coverage.

## License

This project is available under the MIT License.
See LICENSE.
