from abc import ABC, abstractmethod

from src.decorators.error_handling import error_handling


class EmbeddingsStrategy(ABC):
    @error_handling()
    def initialize(self, **kwargs):
        mandatory_fields = ("model",)

        if not all(field in kwargs for field in mandatory_fields):
            raise ValueError(
                "Embeddings Initialization failed: 'model' is a mandatory field."
            )
        
        embedding_callable = self._get_callable()

        kwargs.pop("environment", None)
    
        embedding_instance = embedding_callable(**kwargs)

        return embedding_instance

    @abstractmethod
    def _get_callable(self):
        pass