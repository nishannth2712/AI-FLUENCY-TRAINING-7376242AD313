# Day 1 Task — Gym Membership Assistant: Chatbot vs Workflow vs Agent

**Scenario:** A gym has three membership plans with private pricing that no
public LLM has seen — BASIC = Rs. 1,500/month, PREMIUM = Rs. 2,800/month,
ELITE = Rs. 4,200/month — plus a private 15% discount for paying annually.

## Setup
1. Copy `.env.example` to `.env` and fill in the option you're using
   (Ollama / Groq / Hugging Face) — same as the Day 1 lab.
2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate     # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Run `python check_setup.py` first to confirm the connection works.

## Run each system
```
python chatbot.py     # System 1 — plain LLM, no data
python workflow.py    # System 2 — fixed rules, no LLM
python agent.py        # System 3 — LLM + tools + loop
python challenge.py    # The budget question none of them were designed for
```

Take a screenshot of each run and place it in the `Output/` folder before
pushing to GitHub.

## Files
- `config.py` — provider setup + private gym data
- `check_setup.py` — connection test
- `chatbot.py` — System 1
- `workflow.py` — System 2
- `tools.py` — tool functions used by the agent
- `agent.py` — System 3
- `challenge.py` — the unplanned-for question
- `analysis.md` — full written analysis (see Section 3 of the task brief)
