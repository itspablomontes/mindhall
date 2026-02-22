"""Chat API routes."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.presentation.api.dependencies import ChatServiceDep
from src.presentation.schemas import SendMessageRequest

router = APIRouter(prefix="/agent", tags=["chat"])


@router.post("/chat")
async def send_message(
    request: SendMessageRequest,
    chat_service: ChatServiceDep,
) -> StreamingResponse:
    """Send a message and stream the AI response via SSE."""
    return StreamingResponse(
        chat_service.process_message(
            thread_id=request.thread_id,
            user_id=request.user_id,
            input_text=request.input,
            context=request.context,
            name=request.name,
            perspective=request.perspective,
            style=request.style,
            summary=request.summary,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
