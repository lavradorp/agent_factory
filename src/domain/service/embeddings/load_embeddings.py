from src.domain.service.embeddings.embeddings_strategy import EmbeddingsStrategy
from src.domain.factories.components.embeddings.providers import ProviderType
from src.domain.factories.components.embeddings.registry import embeddings_registry

@embeddings_registry.register(ProviderType.GENERIC)
class LangChainEmbeddingsStrategy(EmbeddingsStrategy):
    def _get_callable(self):
        from langchain.embeddings import init_embeddings

        return init_embeddings


@embeddings_registry.register(ProviderType.GOOGLE)
class GoogleEmbeddingsStrategy(EmbeddingsStrategy):
    def _get_callable(self):
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings

  
@embeddings_registry.register(ProviderType.HUGGING_FACE)
class HuggingFaceEmbeddingsStrategy(EmbeddingsStrategy):
    def _get_callable(self):
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings


@embeddings_registry.register(ProviderType.MISTRAL)
class MistralAIEmbeddingsStrategy(EmbeddingsStrategy):
    def _get_callable(self):
        from langchain_mistralai import MistralAIEmbeddings

        return MistralAIEmbeddings


@embeddings_registry.register(ProviderType.NOMIC)
class NomicEmbeddingsStrategy(EmbeddingsStrategy):
    def _get_callable(self):
        from langchain_nomic import NomicEmbeddings

        return NomicEmbeddings
    

@embeddings_registry.register(ProviderType.OLLAMA)
class OllamaEmbeddingsStrategy(EmbeddingsStrategy):
    def _get_callable(self):
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings
    

@embeddings_registry.register(ProviderType.OPENAI)
class OpenAIEmbeddingsStrategy(EmbeddingsStrategy):
    def _get_callable(self):
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings

