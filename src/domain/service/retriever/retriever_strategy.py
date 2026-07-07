from abc import ABC, abstractmethod

from src.decorators.error_handling import error_handling

class RetrieverStrategy(ABC):
    @abstractmethod
    @error_handling()
    def create(self, vectorstore, **kwargs):
        pass