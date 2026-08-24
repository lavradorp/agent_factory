from src.application.builder.agent.agent_product import AgentProduct
from src.application.builder.agent.base import Builder
from src.domain.factories.components.data.informations.loaders.factory import (
    StrategyDataLoaderFactory,
)
from src.domain.factories.components.data.informations.storage.factory import (
    StrategyDataStorageFactory,
)
from src.domain.factories.components.data.splitters.factory import (
    StrategySplitDataFactory,
)
from src.domain.factories.components.embeddings.factory import StrategyEmbeddingsFactory
from src.domain.factories.components.llm.factory import StrategyLLMsFactory
from src.domain.factories.components.retriever.factory import StrategyRetrieverFactory
from src.domain.factories.components.vector_store.factory import (
    StrategyVectorStoreFactory,
)
from src.domain.models.agent_model import AgentModel


class AgentBuilder(Builder):
    def __init__(self, config: AgentModel):
        self.config = config
        self.reset()

    def reset(self) -> None:
        self._agent = AgentProduct()
    
    @property
    def agent(self) -> AgentProduct:
        product = self._agent

        self.reset()

        return product
    
    def set_llm_model(self) -> None:
        if not self.config.llm:
            return
        
        llm_dict = self.config.llm.model_dump(exclude_none=True)
        provider = llm_dict.pop('provider')

        strategy = StrategyLLMsFactory.execute(
            instance_type=provider,
            
        )

        self._agent.llm = strategy.initialize(**llm_dict)

    def set_embeddings_model(self) -> None:
        if not self.config.embeddings:
            return
        
        embeddings_dict = self.config.embeddings.model_dump(exclude_none=True)
        provider = embeddings_dict.pop('provider')

        strategy = StrategyEmbeddingsFactory.execute(
            instance_type=provider,
        )

        self._agent.embeddings = strategy.initialize(**embeddings_dict)

    def set_vector_store(self) -> None:
        if not self.config.vector_store:
            return
        
        if not self._agent.embeddings:
            raise RuntimeError(
                "Cannot build Vector Store: Embeddings must be defined."
            )
        
        vector_store_dict = self.config.vector_store.model_dump(exclude_none=True)
        engine = vector_store_dict.pop('engine')

        strategy = StrategyVectorStoreFactory.execute(
            instance_type=engine,
        )

        self._agent.vector_store = strategy.create(
            embeddings=self._agent.embeddings,
            **vector_store_dict
            )

    def set_retriever(self) -> None:
        if not self.config.retriever:
            return
            
        if not self._agent.vector_store:
            raise RuntimeError(
                "Cannot build Retriever: Vector Store must be initialized first."
            )

        retriever_dict = self.config.retriever.model_dump(exclude_none=True)
        search_type = retriever_dict.get('search_type')

        strategy = StrategyRetrieverFactory.execute(
            instance_type=search_type
        )

        self._agent.retriever = strategy.create(
            vectorstore=self._agent.vector_store,
            **retriever_dict
        )

    def set_data(self) -> None:
        if not self.config.data_informations:
            return
        
        data_information_dict = self.config.data_informations.model_dump(exclude_none=True)
        
        data_storage = data_information_dict.pop('data_storage')
        data_loaders = data_information_dict.pop('data_loaders')
        data_path = data_information_dict.pop('data_path')

        storage_strategy = StrategyDataStorageFactory.execute(data_storage)
        loader_strategy = StrategyDataLoaderFactory.execute(data_loaders)

        metadata_path = None
        if 'metadata_storage' in list(data_information_dict.keys()):
            metadata_path = data_information_dict.pop('metadata_path')

        with storage_strategy.fetch(data_path) as resolved_path:
            
            raw_documents = loader_strategy.load(
                data_path=str(resolved_path),
                metadata_path=metadata_path
            )

            data_splitter = self.config.data_splitters
            splitter = data_splitter.splitter

            splitter_strategy = StrategySplitDataFactory.execute(
                instance_type=splitter
            )
         
            self._agent.data = splitter_strategy.split(
                documents=raw_documents,
                chunk_size=data_splitter.chunk_size,
                chunk_overlap=data_splitter.chunk_overlap
            )
    
    def set_checkpointer(self) -> None:
        if not self.config.checkpointer:
            return
        
        checkpointer_dict = self.config.checkpointer.model_dump(exclude_none=True)

        self._agent.checkpointer = checkpointer_dict
