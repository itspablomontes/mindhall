"""
FastAPI lifespan events for application startup and shutdown.
Manages initialization of the graph singleton and database connections.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.application.agent.graph_builder import GraphBuilder
from src.application.agent.tools import get_all_tools
from src.infra.llm.client import LLMClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan events.

    On startup:
    - Initialize database connections
    - Build the LangGraph agent (singleton)

    On shutdown:
    - Close database connections
    """
    print("Starting up...")

    # establish db connections here

    llm_client = LLMClient.from_settings()
    tools = get_all_tools()
    graph_builder = GraphBuilder(llm_client=llm_client, tools=tools)
    graph = graph_builder.build()

    app.state.graph = graph
    app.state.llm_client = llm_client

    print("Graph built and ready")
    print(f"Tools available: {[t.name for t in tools]}")

    yield

    # Shutdown
    print("Shutting down...")
    # close db connections here
