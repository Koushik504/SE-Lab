
"""Manage library book loans, renewals, and overdue fines."""

import json
from datetime import datetime

FINE_PER_DAY = 2
loans = {}


def add_book_loan(student_id, book_id, dates=None):
    """Add a book loan using a separate date list for each call."""
    if not student_id:
        return
    if dates is None:
        dates = []
    dates.append(datetime.now().isoformat())
    loans.setdefault(student_id, []).append(book_id)
    print(
        f"{student_id} borrowed {book_id} "
        f"(loan dates on record: {len(dates)})"
    )

def return_book(student_id, book_id):
    """Remove a borrowed book if it exists."""
    student_books = loans.get(student_id, [])
    if book_id not in student_books:
        return
    student_books.remove(book_id)
    if not student_books:
        del loans[student_id]

def calculate_fine(days_overdue):
    """Calculate a fine without allowing negative amounts."""
    return max(0, days_overdue) * FINE_PER_DAY

def renew_book(student_id, book_id, extra_days):
    """Renew a book without changing the global fine rate."""
    if extra_days <= 0:
        raise ValueError("Renewal days must be positive")
    print(f"Renewed {book_id} for {student_id} by {extra_days} days")

def load_records(file="loans.json"):
    """Load book loans from a JSON file."""
    with open(file, "r", encoding="utf-8") as handle:
        saved_loans = json.load(handle)
    loans.clear()
    loans.update(saved_loans)

def save_records(file="loans.json"):
    """Save book loans to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(loans, handle, indent=2)

def fine_from_rule(rule, days):
    """Apply the supported fine rule safely."""
    if rule != "days * 2 + 10":
        raise ValueError("Unsupported fine rule")
    return days * 2 + 10

def print_report():
    """Print all current library loans."""
    print("Loan Report")
    for student_id, student_books in loans.items():
        print(student_id, "->", student_books)

def main():
    """Demonstrate the library management features."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", "4521")
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)

    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))

    user_input = input("Days overdue for S102 (press Enter for 0): ")
    try:
        days = int(user_input or "0")
    except ValueError:
        print("Invalid number of days")
        return

    print("S102 owes:", calculate_fine(days))
    save_records()
    load_records()
    print_report()

if __name__ == "__main__":
    main()
