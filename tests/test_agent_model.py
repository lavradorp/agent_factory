import pytest
from pydantic import ValidationError

from src.domain.models.agent_model import AgentModel

BASE_LLM = {
    "provider": "ollama",
    "model": "llama3.1:8b",
    "temperature": 0.0,
    "environment": "local",
}


def test_llm_only_agent_is_valid():
    model = AgentModel(llm=BASE_LLM)
    assert model.vector_store is None
    assert model.retriever is None


def test_retriever_without_vector_store_is_rejected():
    with pytest.raises(ValidationError):
        AgentModel(
            llm=BASE_LLM,
            retriever={"search_type": "similarity", "top_k": 3},
        )


def test_retriever_with_vector_store_is_valid():
    model = AgentModel(
        llm=BASE_LLM,
        vector_store={
            "engine": "chroma",
            "environment": "local",
            "connection_path": "./vector_store/chroma",
            "collection_name": "agent_metadata_test",
        },
        retriever={"search_type": "similarity", "top_k": 3},
    )
    assert model.retriever.search_type == "similarity"
