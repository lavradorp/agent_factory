import pytest
from pydantic import ValidationError

from src.domain.models.agent_components.vector_store_model import VectorStoreModel


def test_pinecone_does_not_require_connection_path():
    model = VectorStoreModel(
        engine="pinecone",
        environment="cloud",
        collection_name="my-index",
    )
    assert model.connection_path is None


def test_chroma_requires_connection_path():
    with pytest.raises(ValidationError):
        VectorStoreModel(
            engine="chroma",
            environment="local",
            collection_name="my-collection",
        )


def test_chroma_with_connection_path_is_valid():
    model = VectorStoreModel(
        engine="chroma",
        environment="local",
        connection_path="./vector_store/chroma",
        collection_name="my-collection",
    )
    assert model.connection_path == "./vector_store/chroma"


def test_pgvector_requires_connection_path():
    with pytest.raises(ValidationError):
        VectorStoreModel(
            engine="pgvector",
            environment="local",
            collection_name="my-collection",
        )
