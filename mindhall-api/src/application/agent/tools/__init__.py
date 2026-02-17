"""
Agent tools module.
"""

from langchain_core.tools import BaseTool


def get_all_tools() -> list[BaseTool]:
    """
    Get all available tools for the agent.

    Returns:
        List of tool instances
    """
    return []


__all__ = ["get_all_tools"]
