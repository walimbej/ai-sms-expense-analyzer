from app.transaction import get_transactions
from app.report import calculate_total


transactions = get_transactions()

total = calculate_total(transactions)

print("September 2026")
print("-------------------------")
print("ICICI transactions:", len(transactions))
print(f"Total debited: ₹{total:,.2f}")