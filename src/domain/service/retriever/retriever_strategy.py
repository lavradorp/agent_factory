from abc import ABC, abstractmethod

class RetrieverStrategy(ABC):
    @abstractmethod
    def create(self, vectorstore, **kwargs):
        pass