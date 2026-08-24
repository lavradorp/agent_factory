from abc import ABC, abstractmethod

from src.application.builder.agent.agent_product import AgentProduct


class Builder(ABC):
    @abstractmethod
    def set_pipeline(self, agent: AgentProduct, prompts: dict):
        pass
