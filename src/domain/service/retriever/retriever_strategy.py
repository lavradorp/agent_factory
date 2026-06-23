from abc import ABC, abstractmethod
from typing import Dict


class RetrieverStrategy(ABC):
    @abstractmethod
    def create(self, vectorstore, **kwargs):
        pass