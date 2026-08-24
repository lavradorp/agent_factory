from pydantic import BaseModel, Field, model_validator

from src.domain.factories.components.vector_store.engines import EnginesTypes


class VectorStoreModel(BaseModel):
    engine: EnginesTypes
    environment: str = Field(pattern="^(local|cloud)$")
    connection_path: str | None = Field(default=None)
    collection_name: str
    batch_size: int = Field(default=100)
    type: str | None = None

    @model_validator(mode="after")
    def validate_connection_path(self):
        if self.engine == EnginesTypes.PINECONE:
            return self

        if not self.connection_path or not self.connection_path.strip():
            raise ValueError(
                f"The field 'connection_path' is required when engine is '{self.engine.value}'."
            )

        return self
