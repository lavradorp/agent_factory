from contextlib import contextmanager
from pathlib import Path

from src.domain.service.data.informations.storage.data_storage_strategy import DataStorageStrategy
from src.domain.factories.components.data.informations.storage.storage import StorageType
from src.domain.factories.components.data.informations.storage.registry import data_storage_registry


@data_storage_registry.register(StorageType.LOCAL)
class LocalStorageStrategy(DataStorageStrategy):
    @contextmanager
    def fetch(self, source_path: str):
        path_obj = Path(source_path)

        if not path_obj.exists():
            raise FileNotFoundError(f"Path doesn't exists: {source_path}")
        
        yield path_obj

