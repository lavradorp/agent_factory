from pydantic import BaseModel, Field, model_validator
from typing import Optional

from src.domain.factories.components.retriever.search_type import SearchType


class RetrieverModel(BaseModel):
    search_type: SearchType
    top_k: int = Field(default=3, ge=1)
    score_threshold: Optional[float] = Field(default=0.75, ge=0.0, le=1.0)
    # tool_name: Optional[str]
    # description: Optional[str]

    @model_validator(mode="after")
    def validate_retriever_logic(self):
        if self.search_type == SearchType.SIMILARITY_SCORE_THRESHOLD and self.score_threshold is None:
            raise ValueError(
                "The field 'score_threshold' is required when search_type is 'similarity_score_threshold'."
            )
        
        return self
