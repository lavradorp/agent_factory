from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.vector_store.registry import vector_store_registry
import src.domain.service.vector_store.create_vector_store


class StrategyVectorStoreFactory(BaseFactory):

    registry = vector_store_registry