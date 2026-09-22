"""A question none of the three systems was designed for."""
from workflow import workflow
from agent import agent

QUESTION = "I have a budget of Rs. 5000 per month. Which two plans could I combine within this budget?"

print("Q:", QUESTION)
print("\nWorkflow :", workflow(QUESTION))
print("\nAgent    :", agent(QUESTION))
