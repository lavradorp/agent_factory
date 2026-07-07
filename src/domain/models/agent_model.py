from pydantic import BaseModel, model_validator
from typing import Optional

from src.domain.models.agent_components.checkpointer_model import CheckpointerModel
from src.domain.models.agent_components.data.informations_model import DataInformationsModel
from src.domain.models.agent_components.data.splitters_model import DataSplittersModel
from src.domain.models.agent_components.embedding_model import EmbeddingsModel
from src.domain.models.agent_components.llm_model import LLMModel
from src.domain.models.agent_components.retriever_model import RetrieverModel
from src.domain.models.agent_components.vector_store_model import VectorStoreModel


class AgentModel(BaseModel):
    llm: LLMModel
    embeddings: Optional[EmbeddingsModel] = None
    vector_store: Optional[VectorStoreModel] = None
    retriever: Optional[RetrieverModel] = None
    data_informations: Optional[DataInformationsModel] = None
    data_splitters: Optional[DataSplittersModel] = None
    checkpointer: Optional[CheckpointerModel] = None

    @model_validator(mode="after")
    def validate_rag_consistency(self) -> "AgentModel":
        if self.retriever and not self.vector_store:
            raise ValueError("A 'vector_store' must be provided if a 'retriever' is defined.")
        return self