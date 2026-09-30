from app.database import get_september_messages


messages = get_september_messages()

print("September SMS count:", len(messages))