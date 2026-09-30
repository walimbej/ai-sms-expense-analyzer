from app.transaction import get_transactions
from app.report import generate_report


transactions = get_transactions()

print(generate_report(transactions))