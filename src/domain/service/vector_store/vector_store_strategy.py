from abc import ABC, abstractmethod
from pathlib import Path
import shutil

from src.decorators.error_handling import error_handling


class VectorStoreStrategy(ABC):
    @abstractmethod
    @error_handling()
    def create(self, embeddings, **kwargs):
        pass

    @staticmethod
    def reset_database(connection_path: str):
        if Path(connection_path).exists():
            shutil.rmtree(connection_path)
    
    @staticmethod
    def is_empty(connection_path: str) -> bool:
        if not Path(connection_path).exists():
            return True
        return not any(Path(connection_path).iterdir())