from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.data.splitters.registry import data_splitter_registry
import src.domain.service.data.splitters.split_data


class StrategySplitDataFactory(BaseFactory):

    registry = data_splitter_registry
