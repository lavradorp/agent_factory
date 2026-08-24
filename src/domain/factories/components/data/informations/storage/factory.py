import src.domain.service.data.informations.storage.fetch_data  # noqa: F401
from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.data.informations.storage.registry import (
    data_storage_registry,
)


class StrategyDataStorageFactory(BaseFactory):

    registry = data_storage_registry
