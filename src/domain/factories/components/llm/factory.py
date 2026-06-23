from src.domain.factories.base.factory import BaseFactory
from src.domain.factories.components.llm.registry import llm_registry
import src.domain.service.llm.initialize_llm


class StrategyLLMsFactory(BaseFactory):

    registry = llm_registry
