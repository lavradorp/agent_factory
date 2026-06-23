from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.embeddings.registry import embeddings_registry
import src.domain.service.embeddings.load_embeddings


class StrategyEmbeddingsFactory(BaseFactory):

    registry = embeddings_registry
