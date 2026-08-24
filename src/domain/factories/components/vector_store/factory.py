import src.domain.service.vector_store.create_vector_store  # noqa: F401
from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.vector_store.registry import vector_store_registry


class StrategyVectorStoreFactory(BaseFactory):

    registry = vector_store_registry