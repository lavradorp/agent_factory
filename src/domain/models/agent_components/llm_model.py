from pydantic import BaseModel, Field, model_validator
from typing import Optional

from src.domain.factories.components.llm.providers import ProviderType


class LLMModel(BaseModel):
    provider: ProviderType
    model: str
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    environment: str = Field(pattern="^(local|cloud)$")
    base_url: Optional[str] = Field(default=None)
    max_tokens: Optional[int] = Field(default=None)
