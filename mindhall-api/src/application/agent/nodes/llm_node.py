from typing import Any, Sequence, cast

from langchain_core.language_models import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    SystemMessage,
)
from langgraph.graph.state import Runnable, RunnableConfig

from src.application.agent.prompts.mind_character_card_prompt import (
    MIND_CHARACTER_CARD_PROMPT,
)
from src.application.agent.states.agent_state import AgentState


class LLMNode:
    def __init__(
        self, model: BaseChatModel | Runnable[LanguageModelInput, AIMessage]
    ) -> None:
        self.model = model

    async def __call__(
        self, state: AgentState, config: RunnableConfig | None = None
    ) -> dict[str, Any]:
        """Call the LLM with the current state."""
        chat_history = self.mount_chat_history(state)
        response = await self._stream_llm_response(self.model, chat_history, config)
        if response is None:
            return {"messages": []}
        return {"messages": [response]}

    def _build_system_content(self, state: AgentState) -> str:
        """
        Build the system message from state.
        Single place where template + state become the text the model sees.
        """
        template = MIND_CHARACTER_CARD_PROMPT
        return (
            template.replace("{{mind_name}}", state.name)
            .replace("{{mind_perspective}}", state.perspective)
            .replace("{{mind_style}}", state.style)
            .replace("{{mind_context}}", state.context)
            .replace("{{summary}}", state.summary)
        )

    def mount_chat_history(self, state: AgentState) -> Sequence[BaseMessage]:
        """Organize the system prompt based on the state."""
        system_content = self._build_system_content(state)
        return [SystemMessage(content=system_content)] + list(state.messages)

    async def _stream_llm_response(
        self,
        model: BaseChatModel | Runnable[LanguageModelInput, AIMessage],
        messages: Sequence[BaseMessage],
        config: RunnableConfig | None,
    ) -> BaseMessage | None:
        """Stream the LLM response."""
        response = None
        async for chunk in model.astream(messages, config):
            if response is None:
                response = chunk
            else:
                response += chunk
        return cast(BaseMessage | None, response)
