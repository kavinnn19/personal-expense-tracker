import csv
import os

CSV_FILE = "expenses.csv"


def initialize_csv():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "date", "category", "description", "amount"])


def add_expense(date, category, description, amount):
    """Add a new expense to the CSV file."""

    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        expenses = list(reader)

    if expenses:
        new_id = max(int(expense["id"]) for expense in expenses) + 1
    else:
        new_id = 1

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([new_id, date, category, description, amount])


def get_expenses():
    """Return all expenses from the CSV file."""

    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def search_expenses(keyword):
    """Search expenses by description or category."""

    expenses = get_expenses()

    keyword = keyword.lower()

    results = []

    for expense in expenses:
        if (
            keyword in expense["description"].lower()
            or keyword in expense["category"].lower()
        ):
            results.append(expense)

    return results


def filter_by_category(category):
    """Return expenses belonging to a specific category."""

    expenses = get_expenses()

    results = []

    for expense in expenses:
        if expense["category"].lower() == category.lower():
            results.append(expense)

    return results


def delete_expense(expense_id):
    """Delete an expense using its ID."""

    expenses = get_expenses()

    remaining_expenses = []

    deleted = False

    for expense in expenses:
        if int(expense["id"]) == expense_id:
            deleted = True
        else:
            remaining_expenses.append(expense)

    if deleted:
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "id",
                "date",
                "category",
                "description",
                "amount"
            ])

            for expense in remaining_expenses:
                writer.writerow([
                    expense["id"],
                    expense["date"],
                    expense["category"],
                    expense["description"],
                    expense["amount"]
                ])

    return deleted


def calculate_total():
    """Calculate the total amount spent."""

    expenses = get_expenses()

    total = 0

    for expense in expenses:
        total += float(expense["amount"])

    return total


def calculate_category_totals():
    """Calculate total spending for each category."""

    expenses = get_expenses()

    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = float(expense["amount"])

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    return category_totals


def filter_by_date(date):
    """Return expenses for a specific date."""

    expenses = get_expenses()

    results = []

    for expense in expenses:
        if expense["date"] == date:
            results.append(expense)

    return results