




from app.database import get_september_messages


from app.parser import (
    parse_icici_debit,
    parse_icici_upi_mandate,
    parse_hdfc_debit,
    parse_hdfc_successful_payment
)

def get_transactions():
    messages = get_september_messages()

    transactions = []

    for message in messages:
        text = message["text"]

        if not text:
            continue

        transaction = parse_icici_debit(text)

        if not transaction:
            transaction = parse_icici_upi_mandate(text)

        if not transaction:
            transaction = parse_hdfc_debit(text)

        if not transaction:
            transaction = parse_hdfc_successful_payment(text)

        if transaction:
            transaction["message_id"] = message["id"]
            transaction["message_date"] = message["message_date"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # If parser didn't identify a transaction date,
            # use the SMS date as a fallback.
            if not transaction.get("date"):
                transaction["date"] = message["message_date"].strftime(
                    "%Y-%m-%d"
                )

            transactions.append(transaction)

    return transactions

