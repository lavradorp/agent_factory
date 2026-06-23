from abc import ABC, abstractmethod
from contextlib import contextmanager


class DataStorageStrategy(ABC):
    @abstractmethod
    @contextmanager
    def fetch(self):
        pass