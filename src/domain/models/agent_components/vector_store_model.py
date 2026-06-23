from pydantic import BaseModel, Field

from src.domain.factories.components.vector_store.engines import EnginesTypes


class VectorStoreModel(BaseModel):
    engine: EnginesTypes
    environment: str = Field(pattern="^(local|cloud)$")
    connection_path: str
    collection_name: str
    batch_size: int = Field(default=100)
