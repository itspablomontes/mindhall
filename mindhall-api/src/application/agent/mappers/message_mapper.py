"""Mapper: domain Message entities to LangChain message types."""

import json

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from src.domain.entities import Message
from src.domain.value_objects import MessageRole


class MessageMapper:
    """Convert domain Message entities to LangChain messages."""

    @staticmethod
    def to_langchain_messages(messages: list[Message]) -> list[BaseMessage]:
        result: list[BaseMessage] = []
        pending_tool_calls: set[str] = set()

        for msg in messages:
            lc_msg = MessageMapper._convert_single(msg)

            if lc_msg is None:
                continue

            if isinstance(lc_msg, AIMessage):
                pending_tool_calls = {
                    str(tc.get("id") or "") for tc in (lc_msg.tool_calls or [])
                }
                pending_tool_calls = {tc for tc in pending_tool_calls if tc}
                result.append(lc_msg)
                continue

            if isinstance(lc_msg, ToolMessage):
                tool_call_id = str(lc_msg.tool_call_id or "")
                if not pending_tool_calls:
                    continue
                if tool_call_id not in pending_tool_calls:
                    continue
                pending_tool_calls.discard(tool_call_id)
                result.append(lc_msg)
                continue

            if pending_tool_calls:
                pending_tool_calls = set()
            result.append(lc_msg)

        return result

    @staticmethod
    def _convert_single(msg: Message) -> BaseMessage | None:
        match msg.role:
            case MessageRole.HUMAN:
                return HumanMessage(content=msg.content)
            case MessageRole.AI:
                return MessageMapper._convert_ai_message(msg)
            case MessageRole.TOOL:
                return MessageMapper._convert_tool_message(msg)
            case MessageRole.SYSTEM:
                return SystemMessage(content=msg.content)
            case _:
                return None

    @staticmethod
    def _convert_ai_message(msg: Message) -> AIMessage:
        if msg.tool_calls:
            tool_calls = [
                {
                    "id": tc.id,
                    "name": tc.name,
                    "args": json.loads(tc.arguments)
                    if isinstance(tc.arguments, str)
                    else tc.arguments,
                }
                for tc in msg.tool_calls
            ]
            return AIMessage(content=msg.content, tool_calls=tool_calls)
        return AIMessage(content=msg.content)

    @staticmethod
    def _convert_tool_message(msg: Message) -> ToolMessage | None:
        if not msg.tool_call_id:
            return None
        content = msg.tool_result if msg.tool_result else msg.content
        return ToolMessage(
            content=content,
            tool_call_id=msg.tool_call_id,
        )
