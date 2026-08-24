import src.domain.service.checkpointer.start_checkpointer  # noqa: F401
from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.checkpointer.registry import checkpointer_registry


class StrategyCheckpointersFactory(BaseFactory):

    registry = checkpointer_registry
