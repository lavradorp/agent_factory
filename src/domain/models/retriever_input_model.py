from pydantic import BaseModel, Field


class RetrieverInputModel(BaseModel):
    question: str = Field(description="The exact search query to look up.")