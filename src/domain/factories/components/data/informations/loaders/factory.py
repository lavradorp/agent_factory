import src.domain.service.data.informations.loaders.load_data  # noqa: F401
from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.data.informations.loaders.registry import (
    data_loader_registry,
)


class StrategyDataLoaderFactory(BaseFactory):

    registry = data_loader_registry