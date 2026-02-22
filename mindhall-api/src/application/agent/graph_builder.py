"""
Graph builder for the philosopher agent.
"""

from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition

from src.application.agent.edges import should_summarize_conversation
from src.application.agent.nodes.connector import ConnectorNode
from src.application.agent.nodes.llm_node import LLMNode
from src.application.agent.nodes.summarize_context import SummarizeContextNode
from src.application.agent.nodes.summarize_conversation import SummarizeConversationNode
from src.application.agent.nodes.tool import ToolNode
from src.application.agent.states.agent_state import AgentState
from src.infra.llm.client import LLMClient


class GraphBuilder:
    """
    Factory for building the compiled philosopher graph.
    Topology matches philoagents graph.py (conversation → retrieve → summarize_context → loop; connector → summarize_conversation | END).
    """

    def __init__(self, llm_client: LLMClient, tools: list[BaseTool]):
        self.llm_client = llm_client
        self.tools = tools

    def build(self) -> CompiledStateGraph:
        graph = self._build_graph()
        return graph.compile()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(AgentState)
        model = (
            self.llm_client.model.bind_tools(self.tools)
            if self.tools
            else self.llm_client.model
        )

        # Nodes
        graph.add_node("conversation_node", LLMNode(model))
        graph.add_node("retrieve_philosopher_context", ToolNode(self.tools))
        graph.add_node("summarize_context_node", SummarizeContextNode(self.llm_client))
        graph.add_node(
            "summarize_conversation_node", SummarizeConversationNode(self.llm_client)
        )
        graph.add_node("connector_node", ConnectorNode())

        # Edges
        graph.add_edge(START, "conversation_node")
        graph.add_conditional_edges(
            "conversation_node",
            tools_condition,
            {"tools": "retrieve_philosopher_context", END: "connector_node"},
        )
        graph.add_edge("retrieve_philosopher_context", "summarize_context_node")
        graph.add_edge("summarize_context_node", "conversation_node")
        graph.add_conditional_edges(
            "connector_node",
            should_summarize_conversation,
            {"summarize_conversation_node": "summarize_conversation_node", END: END},
        )
        graph.add_edge("summarize_conversation_node", END)

        return graph


def create_graph_builder(llm_client: LLMClient, tools: list[BaseTool]) -> GraphBuilder:
    return GraphBuilder(llm_client=llm_client, tools=tools)
