from abc import ABC, abstractmethod
from src.decorators.error_handling import error_handling


class LLMStrategy(ABC):
    @error_handling()
    # def initialize(self, llm: str, temperature: float, max_tokens=None, base_url=None):
    def initialize(self, **kwargs):
        mandatory_fields = ("model", "temperature")

        if not all(field in kwargs for field in mandatory_fields):
            raise ValueError(
                "LLM Initialization failed: 'model' and 'temperature' are mandatory fields."
            )
        
        llm_callable = self._get_callable()

        kwargs.pop("environment", None)

        llm_initializer = llm_callable(**kwargs)
        
        return llm_initializer

    @abstractmethod
    def _get_callable(self):
        pass