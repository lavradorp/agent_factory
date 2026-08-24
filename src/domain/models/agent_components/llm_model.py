
from pydantic import BaseModel, Field

from src.domain.factories.components.llm.providers import ProviderType


class LLMModel(BaseModel):
    provider: ProviderType
    model: str
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    environment: str = Field(pattern="^(local|cloud)$")
    base_url: str | None = Field(default=None)
    max_tokens: int | None = Field(default=None)
