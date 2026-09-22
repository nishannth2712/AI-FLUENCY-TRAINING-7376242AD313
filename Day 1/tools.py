"""Tools the agent is allowed to use, plus their JSON Schema descriptions."""
import ast
import operator
from config import PLAN_PRICES

def get_plan_price(plan_name: str) -> str:
    """Look up the monthly price for one gym plan (BASIC, PREMIUM or ELITE)."""
    price = PLAN_PRICES.get(plan_name.strip().upper())
    return str(price) if price is not None else f"Unknown plan: {plan_name}"

# A safe calculator: only numbers and + - * / ( ) are allowed. Never use eval().
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg}

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as (1500 + 4200) * 0.85."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"

TOOL_FUNCTIONS = {"get_plan_price": get_plan_price, "calculator": calculator}

# These descriptions are what the LLM reads when deciding which tool to call
TOOLS = [
    {"type": "function", "function": {
        "name": "get_plan_price",
        "description": "Get the monthly price in rupees for a gym plan: BASIC, PREMIUM or ELITE.",
        "parameters": {"type": "object",
                        "properties": {"plan_name": {"type": "string"}},
                        "required": ["plan_name"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object",
                        "properties": {"expression": {"type": "string"}},
                        "required": ["expression"]}}},
]

if __name__ == "__main__":
    print("get_plan_price('premium') ->", get_plan_price("premium"))
    print("calculator('(1500 + 4200) * 0.85') ->", calculator("(1500 + 4200) * 0.85"))
    print("calculator('4200 - 2800') ->", calculator("4200 - 2800"))
