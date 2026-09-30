from app.transaction import get_transactions


transactions = get_transactions()

print("Transactions found:", len(transactions))

for transaction in transactions:
    print(transaction)