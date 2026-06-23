from typing import Dict, Type, Callable, Any


class BaseRegistry:
    def __init__(self, registry_name: str):
        self.registry_name = registry_name
        self._registry: Dict[Any, Type] = {}

    def register(self, *keys: Any) -> Callable:
        def wrapper(wrapped_class: Type) -> Type:
            for key in keys:
                self._registry[key] = wrapped_class
            return wrapped_class
        
        return wrapper

    def get_class(self, key: Any) -> Type:
        if key not in self._registry:
            raise ValueError(
                f"Provider '{key}' is not supported in the '{self.registry_name}' registry."
            )
        return self._registry[key]