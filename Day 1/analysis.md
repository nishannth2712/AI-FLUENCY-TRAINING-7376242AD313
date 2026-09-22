# Analysis: Chatbot vs Rule-Based Workflow vs AI Agent
### Scenario: Gym Membership Pricing Assistant

## 1. The Scenario

A gym offers three membership plans with pricing that is private business
data, not something any public LLM could have seen during training:
BASIC = Rs. 1,500/month, PREMIUM = Rs. 2,800/month, ELITE = Rs. 4,200/month.
The gym also offers a private 15% discount to members who pay for a full
year upfront. I built three systems to answer member questions about this
data — a plain chatbot, a rule-based workflow, and a tool-using AI agent —
and compared how each one behaves.

## 2. Explanation of Each Approach

### 2.1 Plain Chatbot
The chatbot sends the member's question straight to the LLM with no access
to the gym's actual pricing data and no tools of any kind. It relies purely
on the model's language ability to produce a plausible-sounding answer.
Because the model was never trained on this gym's private prices, it either
invents a number (hallucination) or admits it does not know — and it cannot
tell the difference between the two on its own. On my scenario, this showed
up clearly on the pricing questions: the chatbot confidently quoted prices
and totals that had no connection to the real BASIC/PREMIUM/ELITE figures,
while it handled the purely creative question (the motivational message)
well, since that needs no private data at all. Its limitation is structural,
not incidental: no amount of clever prompting gives it access to information
it was never given.

### 2.2 Rule-Based Workflow
The workflow contains no LLM at all — it is ordinary Python code with
fixed `if/else` logic and regular expressions. It looks for plan names in
the question, pulls their prices from a private dictionary, and applies a
hand-written rule for totals and the annual discount. Because the logic is
fixed by the programmer in advance, it produced perfectly correct, instant,
and 100%-repeatable answers for the questions it was designed for (single
plan price, and total with discount). However, it had no rule for comparing
two plans ("is Elite more expensive than Premium, and by how much?") and no
rule for open-ended text generation (the motivational message), so it
correctly reported that it could not help rather than guessing. Its
limitation is rigidity: it only works for exactly the phrasings and
question types its rules anticipated, and a slightly reworded question
(e.g. dropping the word "total") can make a working rule silently fail to
fire.

### 2.3 AI Agent
The agent combines an LLM with two tools — `get_plan_price` (a private data
lookup) and `calculator` (safe arithmetic) — inside a loop. On each turn the
LLM reasons about what it still needs, decides whether to call a tool, and
if so, my Python code (not the LLM) actually executes that tool and returns
the result as an observation; the LLM then reasons again with that new
information, repeating until it can give a final answer. This let the agent
correctly answer every pricing question, including the plan-comparison
question the workflow could not handle, because it wasn't limited to a
pre-written rule — it could look up both prices and then reason about the
difference itself. It also handled the creative question directly, with no
tool call, since the system prompt allows answering without tools when none
are needed. Its limitation is reliability: because the LLM decides the
reasoning path itself, the exact sequence of tool calls (and occasionally
the final wording) can vary between runs, and a weaker model can skip a
tool and guess instead.

## 3. Comparison Table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | High — answers almost any phrasing, but only in the "correct" way if it happens to already know the facts | Low — only works for the exact question shapes its rules anticipate | High — an LLM can interpret new phrasings and combine tools to handle novel questions |
| Decision-making | None — always just generates a response, with no awareness of whether it actually knows the answer | None — a fixed sequence of `if/else` checks decides the path, not the current question's meaning | Yes — the LLM reasons step by step about what to do next and when it has enough information to stop |
| Tool usage | None | None (Python logic acts as the "tool," but it is hard-coded rather than chosen) | Yes — the LLM actively selects and calls tools (price lookup, calculator) as needed |
| Private-data access | None — cannot see the gym's real prices at all | Full — directly reads the private data dictionary | Full — accesses private data only through the tool the programmer exposed to it |
| Multi-step task handling | Poor — treats every question as a single independent generation, cannot combine facts across steps | Poor — can chain at most the one hard-coded sequence (e.g. sum then discount); no arbitrary multi-step reasoning | Strong — loops through as many reason→act→observe steps as needed |
| Automation | Full, but untrustworthy — always produces an answer instantly, with no human check on correctness | Full and trustworthy for its covered cases — instant and deterministic | Full, with more capability but less predictability run-to-run |
| Reliability | Low — confidently wrong on private-data questions, indistinguishable from confidently right | Very high — identical, correct output every time for covered questions; hard failure for uncovered ones | Moderate — correct more often and on harder questions, but the tool-call path and occasionally the answer can vary between runs |

## 4. Suitability Analysis

For this scenario, the **AI agent** is the most suitable approach overall.
The core requirement — answering questions about private, structured gym
pricing, including ones that need a lookup plus arithmetic or a comparison
— is exactly what the workflow's fixed rules could not fully cover (it
failed the plan-comparison question) and what the chatbot could not access
at all (it fabricated prices). The agent was the only system that combined
correct access to the private data with the flexibility to handle a
question its designer hadn't explicitly anticipated.

That said, the workflow is not obsolete here. For the two most common,
predictable member questions — "what does plan X cost" and "what's the
total with the annual discount" — the workflow is faster, free of any LLM
cost, and 100% reliable, which matters if the gym's staff or app needs an
answer they can trust without double-checking. A production system for this
gym would reasonably use the workflow as a fast first pass for known
question shapes, and fall back to the agent for anything the workflow
doesn't recognize.

## 5. Conclusion

In general, a **plain chatbot** is appropriate only when the task needs no
private or up-to-date data and correctness does not hinge on facts the
model could not have learned — creative writing, general explanations, or
brainstorming are good fits. A **rule-based workflow** is the right choice
when the set of questions is small, well-defined, and unlikely to change,
and where perfect, auditable, repeatable behavior matters more than
flexibility — for example, a fixed-format billing calculation or a
regulatory check. An **AI agent** earns its added complexity and reduced
predictability when the task requires combining private data with
reasoning across multiple steps, or when the range of ways a request might
be phrased is too broad to enumerate as fixed rules in advance. The right
choice is rarely "pick one forever" — as this comparison shows, a system
can start with a workflow for the common, well-understood cases and use an
agent as the flexible fallback for everything else.

---
*Note: replace the illustrative behavior described above with the actual
outputs from your own runs (see the `Output/` screenshots), and adjust any
wording here if your model's real answers differ.*
