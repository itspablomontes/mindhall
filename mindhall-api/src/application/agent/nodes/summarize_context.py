"""Summarize retrieved context; return state delta (no in-place mutation)."""

from typing import Any

from langchain_core.messages import HumanMessage

from src.application.agent.prompts.context_summary_prompt import CONTEXT_SUMMARY_PROMPT
from src.application.agent.states.agent_state import AgentState
from src.infra.llm.client import LLMClient


class SummarizeContextNode:
    """Summarizes the last message (tool result) into context; returns state delta."""

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm = llm_client

    async def __call__(self, state: AgentState) -> dict[str, Any]:
        if not state.messages:
            return {}

        last = state.messages[-1]
        raw = getattr(last, "content", str(last))
        last_content = raw if isinstance(raw, str) else str(raw)
        prompt = CONTEXT_SUMMARY_PROMPT.replace("{{context}}", last_content)
        messages = [HumanMessage(content=prompt)]
        response = await self._llm.model.ainvoke(messages)
        summarized = response.content if hasattr(response, "content") else str(response)

        return {"context": summarized}
