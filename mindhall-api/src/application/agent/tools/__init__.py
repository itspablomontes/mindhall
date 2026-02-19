"""
Agent tools module.
"""

from langchain_core.tools import BaseTool

from src.application.agent.tools.sum import sum_numbers


def get_all_tools() -> list[BaseTool]:
    """
    Get all available tools for the agent.

    Returns:
        List of tool instances
    """
    return [sum_numbers]


__all__ = ["get_all_tools"]
