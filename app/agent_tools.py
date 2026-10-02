from app.transaction import get_transactions
from app.report import (
    calculate_total,
    calculate_bank_totals,
    calculate_category_totals,
)


def get_total_debits():
    transactions = get_transactions()

    return {
        "transaction_count": len(transactions),
        "total_debited": calculate_total(transactions),
    }


def get_bank_summary():
    transactions = get_transactions()

    #return calculate_bank_totals(transactions)
    totals = calculate_bank_totals(transactions)

    return {
        bank: round(amount, 2)
        for bank, amount in totals.items()
    }


def get_category_summary():
    transactions = get_transactions()

    #return calculate_category_totals(transactions)

    totals = calculate_category_totals(transactions)

    return {
        category: round(amount, 2)
        for category, amount in totals.items()
    }