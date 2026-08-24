import src.domain.service.retriever.start_retriever  # noqa: F401
from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.retriever.registry import retriever_registry


class StrategyRetrieverFactory(BaseFactory):

    registry = retriever_registry
