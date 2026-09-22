"""Shared configuration: chooses the LLM provider and holds the gym data.

Scenario: A gym has three membership plans with private pricing that no
public LLM has ever seen, plus a private annual-payment discount rule.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads the .env file in this folder

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()

if PROVIDER == "ollama":  # Option A: local model, no key
    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"  # any text works for Ollama
    MODEL = os.getenv("MODEL", "qwen2.5:1.5b")
elif PROVIDER == "groq":  # Option B: free cloud key
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
elif PROVIDER == "huggingface":  # Option C: free cloud key
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
else:
    raise SystemExit(f"Unknown PROVIDER '{PROVIDER}'. Use ollama, groq or huggingface.")

if not API_KEY:
    raise SystemExit(f"No API key found for PROVIDER={PROVIDER}. Check your .env file.")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# ---- Private gym data that no public LLM has ever seen ----
PLAN_PRICES = {"BASIC": 1500, "PREMIUM": 2800, "ELITE": 4200}   # Rs. per month
ANNUAL_DISCOUNT_PERCENT = 15  # applied when paying for a full year upfront

QUESTIONS = [
    "What is the price of the Premium plan?",
    "What is the total cost for Basic and Elite plans combined after a 15% annual discount?",
    "Is the Elite plan more expensive than the Premium plan, and by how much?",
    "Write a two-line motivational message for new gym members.",
]

def banner(system_name):
    print(f"\n=== {system_name} | provider: {PROVIDER} | model: {MODEL} ===\n")
