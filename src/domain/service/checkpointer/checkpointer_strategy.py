from abc import ABC, abstractmethod


class CheckpointerStrategy(ABC):
    @abstractmethod
    def start(self, **kwargs):
        pass