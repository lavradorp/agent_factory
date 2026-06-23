from abc import ABC
from typing import Any

from src.domain.factories.base.registry import BaseRegistry


class BaseFactory(ABC):

    registry: BaseRegistry

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, 'registry'):
            raise TypeError(
                f"Class {cls.__name__} must define a 'registry' class attribute."
            )

    @classmethod
    def execute(cls, instance_type: Any, *args, **kwargs) -> Any:
        strategy_class = cls.registry.get_class(instance_type)
        
        strategy_instance = strategy_class()
        
        return cls._post_initialization(strategy_instance, *args, **kwargs)
    
    @classmethod
    def _post_initialization(cls, strategy_instance: Any, *args, **kwargs) -> Any:
        return strategy_instance