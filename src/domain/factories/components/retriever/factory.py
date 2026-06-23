from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.retriever.registry import retriever_registry
import src.domain.service.retriever.start_retriever


class StrategyRetrieverFactory(BaseFactory):

    registry = retriever_registry
