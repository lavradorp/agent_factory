from abc import ABC, abstractmethod


class Builder(ABC):

    @property
    @abstractmethod
    def agent(self):
        pass
    
    @abstractmethod
    def set_llm_model(self):
        pass

    @abstractmethod
    def set_embeddings_model(self):
        pass

    @abstractmethod
    def set_vector_store(self):
        pass

    @abstractmethod
    def set_retriever(self):
        pass

    @abstractmethod
    def set_data(self):
        pass