from abc import ABC, abstractmethod
from pathlib import Path
import shutil


class VectorStoreStrategy(ABC):
    @abstractmethod
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