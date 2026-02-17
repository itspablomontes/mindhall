from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True,
    )

    total_messages_after_summary: int = 10

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    app_env: str = "development"
    debug: bool = True

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v: str | bool) -> bool:
        """Parse debug value, handling string 'true'/'false' and ignoring invalid values."""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            lower = v.lower()
            if lower in ("true", "1", "yes", "on"):
                return True
            elif lower in ("false", "0", "no", "off"):
                return False
        return True

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
