
import requests
import json

from app.agent_tools import (
    get_total_debits,
    get_bank_summary,
    get_category_summary,
)


LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"


TOOLS = {
    "get_total_debits": get_total_debits,
    "get_bank_summary": get_bank_summary,
    "get_category_summary": get_category_summary,
}


def ask_llm(question):
    prompt = f"""
You are a financial assistant.

Choose the correct tool for the user's question.

Available tools:

1. get_total_debits
   Use for questions about total spending.

2. get_bank_summary
   Use for questions about spending through a particular bank.
   Available banks: ICICI, HDFC.

3. get_category_summary
   Use for questions about spending categories.

Return ONLY valid JSON.

For total spending:

{{
    "tool": "get_total_debits",
    "arguments": {{}}
}}

For bank questions:

{{
    "tool": "get_bank_summary",
    "arguments": {{
        "bank": "ICICI"
    }}
}}

For category questions:

{{
    "tool": "get_category_summary",
    "arguments": {{}}
}}

User question:
{question}
"""

    response = requests.post(
        LLM_URL,
        json={
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0,
            "max_tokens": 150
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    content = data["choices"][0]["message"]["content"].strip()

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    return content


def run_agent(question):
    llm_response = ask_llm(question)

    try:
        decision = json.loads(llm_response)

    except json.JSONDecodeError:
        return {
            "error": "LLM returned invalid JSON",
            "llm_response": llm_response
        }

    tool_name = decision.get("tool")
    arguments = decision.get("arguments", {})

    if tool_name not in TOOLS:
        return {
            "error": "Unknown tool",
            "tool": tool_name
        }

    if tool_name == "get_total_debits":

        result = TOOLS[tool_name]()

        answer = (
            f"In September 2026, you spent a total of "
            f"₹{result['total_debited']:,.2f}."
        )

    elif tool_name == "get_bank_summary":

        result = TOOLS[tool_name]()

        bank = arguments.get("bank")

        if bank:
            bank = bank.upper()

            amount = result.get(bank, 0)

            result = {
                bank: amount
            }

            answer = (
                f"In September 2026, you spent "
                f"₹{amount:,.2f} through {bank}."
            )

        else:
            answer = "Here is your spending by bank:"

            for bank_name, amount in result.items():
                answer += (
                    f"\n{bank_name}: ₹{amount:,.2f}"
                )

    elif tool_name == "get_category_summary":

        result = TOOLS[tool_name]()

        answer = "In September 2026, your spending by category was:"

        for category, amount in sorted(
            result.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            answer += (
                f"\n{category}: ₹{amount:,.2f}"
            )

    else:

        result = None
        answer = "I couldn't process that request."

    return {
        "question": question,
        "tool": tool_name,
        "arguments": arguments,
        "result": result,
        "answer": answer
    }