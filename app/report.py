def calculate_total(transactions):
    return sum(transaction["amount"] for transaction in transactions)