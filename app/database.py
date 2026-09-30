
import sqlite3
from datetime import datetime

DB_PATH = "data/sms.db"


def get_september_messages():
    connection = sqlite3.connect(DB_PATH)

    query = """
        SELECT ROWID, date, text
        FROM message
        WHERE service = 'SMS'
        AND date >= (strftime('%s','2026-09-01') - 978307200) * 1000000000
        AND date < (strftime('%s','2026-10-01') - 978307200) * 1000000000
        ORDER BY date
    """

    rows = connection.execute(query).fetchall()
    connection.close()

    messages = []

    for rowid, apple_date, text in rows:
        unix_timestamp = apple_date / 1_000_000_000 + 978307200
        message_date = datetime.fromtimestamp(unix_timestamp)

        messages.append({
            "id": rowid,
            "message_date": message_date,
            "text": text,
        })

    return messages