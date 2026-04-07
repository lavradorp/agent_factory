from pydantic import BaseModel, Field, model_validator


class LLMConfigModel(BaseModel):
    provider: str = Field(pattern="^(google|openai|anthropic|ollama|mistral)$")
    type: str = Field(pattern="^(local|cloud)$")
    model: str
    embedding_model: str
    base_url: str | None = None
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    api_key: str | None = None

    @model_validator(mode='after')
    def validar_cloud_api_key(self):
        if self.type == "cloud" and not self.api_key:
            raise ValueError(f"You must set a API Key for cloud models.")
        return self