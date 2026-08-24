import pytest

from src.domain.factories.components.checkpointer.factory import (
    StrategyCheckpointersFactory,
)
from src.domain.factories.components.checkpointer.savers import SaverType
from src.domain.factories.components.embeddings.factory import StrategyEmbeddingsFactory
from src.domain.factories.components.embeddings.providers import (
    ProviderType as EmbeddingsProviderType,
)
from src.domain.factories.components.llm.factory import StrategyLLMsFactory
from src.domain.factories.components.llm.providers import (
    ProviderType as LLMProviderType,
)
from src.domain.factories.components.retriever.factory import StrategyRetrieverFactory
from src.domain.factories.components.retriever.search_type import SearchType
from src.domain.factories.components.vector_store.engines import EnginesTypes
from src.domain.factories.components.vector_store.factory import (
    StrategyVectorStoreFactory,
)


@pytest.mark.parametrize("provider", list(LLMProviderType))
def test_llm_registry_resolves_every_provider(provider):
    strategy = StrategyLLMsFactory.execute(instance_type=provider)
    assert strategy is not None


@pytest.mark.parametrize("provider", list(EmbeddingsProviderType))
def test_embeddings_registry_resolves_every_provider(provider):
    strategy = StrategyEmbeddingsFactory.execute(instance_type=provider)
    assert strategy is not None


@pytest.mark.parametrize("engine", list(EnginesTypes))
def test_vector_store_registry_resolves_every_engine(engine):
    strategy = StrategyVectorStoreFactory.execute(instance_type=engine)
    assert strategy is not None


@pytest.mark.parametrize("saver", list(SaverType))
def test_checkpointer_registry_resolves_every_saver(saver):
    strategy = StrategyCheckpointersFactory.execute(instance_type=saver)
    assert strategy is not None


@pytest.mark.parametrize("search_type", list(SearchType))
def test_retriever_registry_resolves_every_search_type(search_type):
    strategy = StrategyRetrieverFactory.execute(instance_type=search_type)
    assert strategy is not None


def test_llm_registry_raises_on_unknown_provider():
    with pytest.raises(ValueError):
        StrategyLLMsFactory.execute(instance_type="not-a-real-provider")


def test_vector_store_registry_raises_on_unknown_engine():
    with pytest.raises(ValueError):
        StrategyVectorStoreFactory.execute(instance_type="not-a-real-engine")
