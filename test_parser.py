from app.parser import parse_icici_debit


sms = """
ICICI Bank Acct XXxxx debited for Rs 603.00 on 27-Sep-26; Zepto credited.
"""

result = parse_icici_debit(sms)

print(result)