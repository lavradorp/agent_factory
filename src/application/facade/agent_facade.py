from src.adapters.loaders.yaml_loader import YAMLLoader

from src.application.builder.agent.agent_builder import AgentBuilder
from src.application.builder.agent.agent_product import AgentProduct

from src.domain.models.agent_model import AgentModel

class AgentFacade:
    
    @staticmethod
    def build_from_yaml(config_model: AgentModel) -> AgentProduct:
        builder = AgentBuilder(config=config_model)

        builder.set_llm_model()

        if config_model.embeddings:
            builder.set_embeddings_model()

            builder.set_vector_store()

            builder.set_retriever()

        builder.set_checkpointer()


        return builder.agent
    
    