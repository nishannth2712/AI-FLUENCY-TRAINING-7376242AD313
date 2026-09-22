"""System 2: a rule-based workflow. Fixed if/else rules, no LLM at all."""
import re
from config import PLAN_PRICES, ANNUAL_DISCOUNT_PERCENT

def workflow(question):
    text = question.upper()
    plans = [name for name in PLAN_PRICES if name in text]
    prices = [PLAN_PRICES[name] for name in plans]

    if not prices:
        return "Sorry, I can only answer questions about BASIC, PREMIUM or ELITE plans."

    lower = question.lower()
    if "total" in lower or "combined" in lower:
        total = sum(prices)
        if "discount" in lower or "annual" in lower:
            total = total * (1 - ANNUAL_DISCOUNT_PERCENT / 100)
        return f"Total cost: Rs. {total:,.0f}"

    if len(prices) == 1:
        return f"Price of {plans[0].title()} plan: Rs. {prices[0]:,}"

    return "Sorry, I do not have a rule for this type of question."

if __name__ == "__main__":
    from config import QUESTIONS
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (no LLM) ===\n")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)
