"""FastAPI dependencies for dependency injection."""

from typing import Annotated

from fastapi import Depends, Request
from langgraph.graph.state import CompiledStateGraph
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.application.agent.states.agent_state import AgentState
from src.application.services import (
    ChatService,
    ThreadService,
    create_chat_service,
    create_thread_service,
)
from src.infra.database.connection import get_database
from src.infra.database.repositories.message_repository_impl import (
    MessageRepositoryImpl,
)
from src.infra.database.repositories.thread_repository_impl import (
    ThreadRepositoryImpl,
)


def get_db() -> AsyncIOMotorDatabase:
    """Return the application MongoDB database (from lifespan-initialized connection)."""
    return get_database()


def get_graph(request: Request) -> CompiledStateGraph[AgentState]:
    """Return the compiled graph from app state."""
    return request.app.state.graph


def get_message_repository(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> MessageRepositoryImpl:
    return MessageRepositoryImpl(db)


def get_thread_repository(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> ThreadRepositoryImpl:
    return ThreadRepositoryImpl(db)


def get_chat_service(
    graph: Annotated[CompiledStateGraph[AgentState], Depends(get_graph)],
    message_repo: Annotated[MessageRepositoryImpl, Depends(get_message_repository)],
    thread_repo: Annotated[ThreadRepositoryImpl, Depends(get_thread_repository)],
) -> ChatService:
    return create_chat_service(
        graph=graph,
        message_repository=message_repo,
        thread_repository=thread_repo,
    )


def get_thread_service(
    message_repo: Annotated[MessageRepositoryImpl, Depends(get_message_repository)],
    thread_repo: Annotated[ThreadRepositoryImpl, Depends(get_thread_repository)],
) -> ThreadService:
    return create_thread_service(
        message_repository=message_repo,
        thread_repository=thread_repo,
    )


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
ThreadServiceDep = Annotated[ThreadService, Depends(get_thread_service)]
