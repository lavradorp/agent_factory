from typing import Optional

from pydantic import BaseModel, Field, model_validator

from src.domain.factories.components.embeddings.providers import ProviderType


class EmbeddingsModel(BaseModel):
    provider: ProviderType
    model: str
    environment: str = Field(pattern="^(local|cloud)$")
