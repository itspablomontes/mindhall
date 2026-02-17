"""
LLM Client wrapper
"""

from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from src.infra.config import get_settings


class LLMClient:
    """
    Wrapper around LangChain ChatOpenAI.
    Provides a consistent interface for LLM interactions.
    """

    def __init__(self, model: ChatOpenAI):
        self.model = model

    @classmethod
    def from_settings(cls) -> "LLMClient":
        """
        Create LLMClient from application settings.

        Returns:
            Configured LLMClient instance
        """
        settings = get_settings()

        model = ChatOpenAI(
            api_key=SecretStr(settings.openai_api_key),
            model=settings.openai_model,
            temperature=0.7,
            streaming=True,
        )

        return cls(model=model)
