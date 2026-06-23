from typing import Optional
from pydantic import BaseModel, Field


class DataSplittersModel(BaseModel):
    splitter: str
    chunk_size: int = Field(default=100)
    chunk_overlap: Optional[int] = Field(default=0)