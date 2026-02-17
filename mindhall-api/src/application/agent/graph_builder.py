"""
Graph builder factory for creating the compiled LangGraph agent.
"""

from langchain_core.tools import BaseTool
from langgraph.graph.state import CompiledStateGraph
from src.application.agent.graph import create_agent_graph
from src.infra.llm.client import LLMClient


class GraphBuilder:
    """
    Factory for building compiled LangGraph agents.

    The builder receives dependencies (LLM client, tools) and produces
    a compiled graph that is stateless and can be shared between requests.
    """

    def __init__(self, llm_client: LLMClient, tools: list[BaseTool]):
        """
        Initialize the graph builder.

        Args:
            llm_client: LLM client for model calls
            tools: List of tools available to the agent
        """
        self.llm_client = llm_client
        self.tools = tools

    def build(self) -> CompiledStateGraph:
        """
        Build and compile the agent graph.

        Returns:
            Compiled StateGraph ready for execution.
            This graph is stateless and can be reused across requests.
        """
        graph = create_agent_graph(llm_client=self.llm_client, tools=self.tools)

        compiled = graph.compile()

        return compiled
