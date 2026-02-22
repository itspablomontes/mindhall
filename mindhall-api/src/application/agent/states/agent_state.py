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
    Event emitted during streaming (SSE envelope).
    Used by orchestrator and frontend; event + data only.
    """

    event: str
    data: dict = Field(default_factory=dict)
