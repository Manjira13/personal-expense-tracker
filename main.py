"""Command-line interface for the Personal Expense Tracker."""

from datetime import date
from decimal import Decimal, InvalidOperation

from expense_tracker.database import initialize_database
from expense_tracker.expense_manager import ExpenseManager
from expense_tracker.models import Transaction

CURRENCY = "₹"


def prompt_date(prompt: str, allow_blank: bool = False):
    raw = input(prompt).strip()

    if allow_blank and not raw:
        return None

    try:
        return date.fromisoformat(raw)
    except ValueError:
        raise ValueError(
            "Enter a valid date in YYYY-MM-DD format."
        )


def prompt_transaction(existing: Transaction = None) -> Transaction:
    title = input(
        f"Title [{existing.title if existing else ''}]: "
    ).strip()

    if existing and not title:
        title = existing.title

    amount_text = input(
        f"Amount [{existing.amount if existing else ''}]: "
    ).strip()

    if existing and not amount_text:
        amount = existing.amount
    else:
        try:
            amount = Decimal(amount_text)
        except InvalidOperation:
            raise ValueError("Enter a valid amount.")

    type_text = input(
        f"Type income/expense "
        f"[{existing.transaction_type if existing else ''}]: "
    ).strip()

    transaction_type = type_text or (
        existing.transaction_type if existing else ""
    )

    category = input(
        f"Category [{existing.category if existing else ''}]: "
    ).strip()

    category = category or (
        existing.category if existing else ""
    )

    date_text = input(
        f"Date YYYY-MM-DD "
        f"[{existing.transaction_date if existing else date.today()}]: "
    ).strip()

    if existing and not date_text:
        transaction_date = existing.transaction_date
    else:
        try:
            transaction_date = (
                date.fromisoformat(date_text)
                if date_text else date.today()
            )
        except ValueError:
            raise ValueError(
                "Enter a valid date in YYYY-MM-DD format."
            )

    notes = input(
        f"Notes [{existing.notes if existing else ''}]: "
    ).strip()

    if existing and not notes:
        notes = existing.notes

    return Transaction(
        title,
        amount,
        transaction_type,
        category,
        transaction_date,
        notes
    )


def display_transactions(transactions):
    if not transactions:
        print("\nNo transactions found.")
        return

    print(
        "\n{:<5} {:<12} {:<24} {:>12} {:<9} {:<16} {}".format(
            "ID", "Date", "Title", "Amount",
            "Type", "Category", "Notes"
        )
    )

    print("-" * 100)

    for item in transactions:
        print(
            "{:<5} {:<12} {:<24} {:>12} {:<9} {:<16} {}".format(
                item.transaction_id,
                item.transaction_date.isoformat(),
                item.title[:23],
                f"{CURRENCY}{item.amount:.2f}",
                item.transaction_type,
                item.category[:15],
                item.notes
            )
        )


def show_summary(summary):
    print(f"Income:   {CURRENCY}{summary['income']:.2f}")
    print(f"Expenses: {CURRENCY}{summary['expenses']:.2f}")
    print(f"Balance:  {CURRENCY}{summary['balance']:.2f}")


def main():
    initialize_database()
    manager = ExpenseManager()

    actions = {
        "1": "Add transaction",
        "2": "View transactions",
        "3": "Update transaction",
        "4": "Delete transaction",
        "5": "Filter transactions",
        "6": "Overall summary",
        "7": "Monthly summary",
        "0": "Exit",
    }

    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")

        for key, label in actions.items():
            print(f"{key}. {label}")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                transaction = prompt_transaction()
                transaction_id = manager.add_transaction(transaction)

                print(
                    f"Transaction added successfully "
                    f"(ID: {transaction_id})."
                )

            elif choice == "2":
                display_transactions(
                    manager.get_all_transactions()
                )

            elif choice == "3":
                transaction_id = int(
                    input("Enter transaction ID: ")
                )

                existing = manager.get_transaction(transaction_id)

                if not existing:
                    print("Transaction not found.")
                    continue

                updated = prompt_transaction(existing)

                print(
                    "Transaction updated."
                    if manager.update_transaction(
                        transaction_id, updated
                    )
                    else "Transaction not found."
                )

            elif choice == "4":
                transaction_id = int(
                    input("Enter transaction ID: ")
                )

                confirm = input(
                    "Delete this transaction? (y/n): "
                ).strip().lower()

                if confirm == "y":
                    print(
                        "Transaction deleted."
                        if manager.delete_transaction(transaction_id)
                        else "Transaction not found."
                    )

            elif choice == "5":
                start = prompt_date(
                    "Start date YYYY-MM-DD (blank to skip): ", True
                )

                end = prompt_date(
                    "End date YYYY-MM-DD (blank to skip): ", True
                )

                category = (
                    input("Category (blank to skip): ").strip()
                    or None
                )

                transaction_type = (
                    input("Type income/expense (blank to skip): ").strip()
                    or None
                )

                if start and end and start > end:
                    raise ValueError(
                        "Start date cannot be after end date."
                    )

                display_transactions(
                    manager.filter_transactions(
                        start, end, category, transaction_type
                    )
                )

            elif choice == "6":
                show_summary(manager.overall_summary())

            elif choice == "7":
                year = int(input("Year (e.g. 2026): "))
                month = int(input("Month (1-12): "))

                show_summary(
                    manager.monthly_summary(year, month)
                )

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print(
                    "Invalid option. Please choose one "
                    "of the listed options."
                )

        except (ValueError, TypeError) as error:
            print(f"Error: {error}")

        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
