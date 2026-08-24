from abc import ABC, abstractmethod


class DataSplitterStrategy(ABC):
    @abstractmethod
    def split(self, documents: list, chunk_size: int, chunk_overlap: int = 0):
        pass
