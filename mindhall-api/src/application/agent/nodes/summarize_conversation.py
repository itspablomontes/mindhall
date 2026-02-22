"""Summarize conversation; return state delta with new summary and optional message trim."""

from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.graph.message import RemoveMessage

from src.application.agent.prompts.extend_summary_prompt import EXTEND_SUMMARY_PROMPT
from src.application.agent.prompts.summary_prompt import SUMMARY_PROMPT
from src.application.agent.states.agent_state import AgentState
from src.infra.config import get_settings
from src.infra.llm.client import LLMClient


class SummarizeConversationNode:
    """Builds conversation summary via LLM; returns {summary, messages: [RemoveMessage, ...]}."""

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm = llm_client

    async def __call__(self, state: AgentState) -> dict[str, Any]:
        summary_prompt = self._build_summary_prompt(state)

        # Use last N messages as context for the summary
        messages_for_summary = (
            state.messages[-20:] if len(state.messages) > 20 else state.messages
        )
        text = "\n".join(getattr(m, "content", str(m)) for m in messages_for_summary)

        full_prompt = f"{summary_prompt}\n\nConversation:\n{text}"
        response = await self._llm.model.ainvoke([HumanMessage(content=full_prompt)])
        new_summary = (
            response.content if hasattr(response, "content") else str(response)
        )

        settings = get_settings()
        keep = settings.total_messages_after_summary
        to_remove = state.messages[:-keep] if len(state.messages) > keep else []
        remove_messages = [
            RemoveMessage(id=mid) for m in to_remove if (mid := getattr(m, "id", None))
        ]
        return {"summary": new_summary, "messages": remove_messages}

    def _build_summary_prompt(self, state: AgentState) -> str:
        if len(state.summary) > 0:
            return EXTEND_SUMMARY_PROMPT.replace("{{mind_name}}", state.name).replace(
                "{{summary}}", state.summary
            )
        return SUMMARY_PROMPT.replace("{{mind_name}}", state.name)
