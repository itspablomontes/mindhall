"""
Graph builder factory for creating the compiled LangGraph agent.
"""

from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition
from src.application.agent.nodes.llm_node import LLMNode
from src.application.agent.nodes.tool import ToolNode
from src.application.agent.states.agent_state import AgentState
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
        graph = self._build_graph(llm_client=self.llm_client, tools=self.tools)

        compiled = graph.compile()

        return compiled

    def _build_graph(self, llm_client: LLMClient, tools: list[BaseTool]) -> StateGraph:

        graph = StateGraph(AgentState)

        model = llm_client.model.bind_tools(tools) if tools else llm_client.model

        graph.add_node("agent", LLMNode(model))
        graph.add_node("tools", ToolNode(tools))

        graph.add_edge(START, "agent")
        graph.add_conditional_edges(
            "agent", tools_condition, {"tools": "tools", END: END}
        )
        graph.add_edge("tools", "agent")

        return graph


def create_graph_builder(llm_client: LLMClient, tools: list[BaseTool]) -> GraphBuilder:
    """
    Create a new GraphBuilder instance.

    Args:
        llm_client: LLM client for model calls
        tools: List of tools available to the agent

    Returns:
        Configured GraphBuilder
    """
    return GraphBuilder(llm_client=llm_client, tools=tools)
