
from pydantic import BaseModel, Field


class DataSplittersModel(BaseModel):
    splitter: str
    chunk_size: int = Field(default=100)
    chunk_overlap: int | None = Field(default=0)