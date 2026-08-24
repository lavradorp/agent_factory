import src.domain.service.data.splitters.split_data  # noqa: F401
from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.data.splitters.registry import (
    data_splitter_registry,
)


class StrategySplitDataFactory(BaseFactory):

    registry = data_splitter_registry
