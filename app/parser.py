import re
from datetime import datetime


def parse_icici_debit(text):
    pattern = (
        r"ICICI Bank.*?"
        r"debited for Rs\.?\s*([\d,]+(?:\.\d{2})?)"
        r".*?on\s+(\d{1,2}-[A-Za-z]{3}-\d{2});"
        r"\s*(.*?)\s+credited"
    )

    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return None

    amount = float(match.group(1).replace(",", ""))
    date = datetime.strptime(match.group(2), "%d-%b-%y")
    merchant = match.group(3).strip()

    return {
        "bank": "ICICI",
        "type": "debit",
        "amount": amount,
        "date": date.strftime("%Y-%m-%d"),
        "merchant": merchant,
    }


def parse_icici_upi_mandate(text):
    import re
    from datetime import datetime

    match = re.search(
        r"Rs\.?\s*([\d,]+(?:\.\d{2})?)"
        r"\s+debited\s+from\s+ICICI\s+Bank.*?"
        r"on\s+(\d{1,2}-[A-Za-z]{3}-\d{2})"
        r"\s+towards\s+(.+?)"
        r"\s+for\s+UPI\s+Mandate",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    amount = float(match.group(1).replace(",", ""))
    date = datetime.strptime(match.group(2), "%d-%b-%y")
    merchant = match.group(3).strip()

    return {
        "bank": "ICICI",
        "type": "debit",
        "amount": amount,
        "date": date.strftime("%Y-%m-%d"),
        "merchant": merchant,
        "source_type": "icici_upi_mandate",
    }



def parse_hdfc_debit(text):
    import re
    from datetime import datetime

    # HDFC NEFT / account debit
    match = re.search(
        r"Amt Deducted.*?Rs\.?\s*([\d,]+(?:\.\d{2})?).*?HDFC Bank",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return {
            "bank": "HDFC",
            "type": "debit",
            "amount": float(match.group(1).replace(",", "")),
            "date": None,
            "merchant": "NEFT",
        }

    # HDFC debit-card transaction
    match = re.search(
        r"(?:Spent|spent).*?Rs\.?\s*([\d,]+(?:\.\d{2})?).*?"
        r"HDFC Bank Card.*?At\s+(.+?)\s+On\s+",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return {
            "bank": "HDFC",
            "type": "debit",
            "amount": float(match.group(1).replace(",", "")),
            "date": None,
            "merchant": match.group(2).strip(),
        }

    return None

def parse_hdfc_successful_payment(text):
    import re

    match = re.search(
        r"Payment Successful!\s*Rs\.?\s*([\d,]+(?:\.\d{2})?)"
        r".*?to\s+(.+?)\s+via\s+HDFC Bank NetBanking",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    return {
        "bank": "HDFC",
        "type": "debit",
        "amount": float(match.group(1).replace(",", "")),
        "date": None,
        "merchant": match.group(2).strip(),
        "source_type": "hdfc_netbanking",
    }