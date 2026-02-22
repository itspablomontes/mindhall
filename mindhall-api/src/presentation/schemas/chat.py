"""Pydantic schemas for chat API."""

from pydantic import BaseModel, Field


class SendMessageRequest(BaseModel):
    """Request body for POST /chat: user message and mind context."""

    input: str = Field(..., description="The user's message text")
    thread_id: str = Field(..., description="Conversation thread ID")
    user_id: str = Field(..., description="User ID")
    context: str = Field(default="", description="Mind context (retrieved/summarized)")
    name: str = Field(default="", description="Mind name / character")
    perspective: str = Field(default="", description="Mind perspective")
    style: str = Field(default="", description="Mind style")
    summary: str = Field(default="", description="Conversation summary so far")
