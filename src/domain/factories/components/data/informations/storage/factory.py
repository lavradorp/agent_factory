from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.data.informations.storage.registry import data_storage_registry
import src.domain.service.data.informations.storage.fetch_data


class StrategyDataStorageFactory(BaseFactory):

    registry = data_storage_registry
