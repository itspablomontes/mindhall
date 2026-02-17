from typing import Annotated
from langgraph.graph import add_messages
from langgraph.graph.message import BaseMessage
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    State schema for the LangGraph agent.

    This state is isolated per execution - each graph.stream() call
    creates its own state instance.
    """

    thread_id: str
    user_id: str
    messages: Annotated[list[BaseMessage], add_messages] = Field(default_factory=list)
    context: str
    name: str
    perspective: str
    style: str
    summary: str

    class Config:
        arbitrary_types_allowed = True


class StreamEvent(BaseModel):
    """
    Event emitted during streaming.
    Used to communicate with the frontend via SSE.

    Mirrors LangChain astream_events v2 envelope where possible.
    """

    event: str
    name: str | None = None
    run_id: str | None = None
    parent_ids: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    data: dict = Field(default_factory=dict)
