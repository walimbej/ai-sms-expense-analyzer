
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.transaction import get_transactions
from app.report import (
    calculate_total,
    calculate_bank_totals,
    calculate_category_totals,
)
from app.agent import run_agent


app = FastAPI(title="AI Financial Assistant")


@app.get("/")
def home():
    return {
        "message": "AI Financial Assistant is running"
    }


@app.get("/summary")
def summary():
    transactions = get_transactions()

    return {
        "transaction_count": len(transactions),
        "total_debited": calculate_total(transactions),
        "by_bank": calculate_bank_totals(transactions),
        "by_category": calculate_category_totals(transactions),
    }


@app.get("/transactions")
def transactions():
    return get_transactions()


@app.get("/ask")
def ask(question: str):
    return run_agent(question)


@app.get("/web")
def web():
    return FileResponse("app/static/index.html")