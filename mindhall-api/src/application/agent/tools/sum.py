from langchain_core.tools import tool


@tool
def sum_numbers(a: int, b: int) -> int:
    return a + b
