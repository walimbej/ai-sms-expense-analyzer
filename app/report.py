

from collections import defaultdict


def calculate_total(transactions):
    return sum(transaction["amount"] for transaction in transactions)


def calculate_bank_totals(transactions):
    totals = defaultdict(float)

    for transaction in transactions:
        totals[transaction["bank"]] += transaction["amount"]

    return dict(totals)


def categorize_transaction(transaction):
    merchant = transaction["merchant"].lower()

    if any(word in merchant for word in [
        "zepto",
        "blinkit",
        "zomato",
        "amazon",
        "chitale",
        "grocer",
        "vegetab",
        "pure n sure",
    ]):
        return "Shopping & Food"

    if "microsoft" in merchant:
        return "Subscriptions & Software"

    if "openai" in merchant:
        return "Subscriptions & Software"

    if "lic of india" in merchant:
        return "Insurance"

    if "maharashtra ele" in merchant:
        return "Utilities"

    if "chintamani" in merchant:
        return "Personal Transfer"

    if "aaryaswalimbe" in merchant:
        return "Personal Transfer"

    return "Other"


def calculate_category_totals(transactions):
    totals = defaultdict(float)

    for transaction in transactions:
        category = categorize_transaction(transaction)
        totals[category] += transaction["amount"]

    return dict(totals)


def generate_report(transactions):
    total = calculate_total(transactions)
    bank_totals = calculate_bank_totals(transactions)
    category_totals = calculate_category_totals(transactions)

    report = []

    report.append("September 2026 Expense Report")
    report.append("=" * 32)
    report.append(f"Transactions: {len(transactions)}")
    report.append(f"Total debited: ₹{total:,.2f}")

    report.append("")
    report.append("By Bank")
    report.append("-" * 32)

    for bank, amount in sorted(bank_totals.items()):
        report.append(f"{bank}: ₹{amount:,.2f}")

    report.append("")
    report.append("By Category")
    report.append("-" * 32)

    for category, amount in sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        report.append(f"{category}: ₹{amount:,.2f}")

    return "\n".join(report)