from src.domain.service.llm.llm_strategy import LLMStrategy
from src.domain.factories.components.llm.providers import ProviderType
from src.domain.factories.components.llm.registry import llm_registry


@llm_registry.register(ProviderType.GENERIC)
class LangChainLLMStrategy(LLMStrategy):
    def _get_callable(self):
        from langchain.chat_models import init_chat_model
        
        return init_chat_model
    

@llm_registry.register(ProviderType.ANTHROPIC)
class AnthropicLLMStrategy(LLMStrategy):
    def _get_callable(self):
        from langchain_anthropic import ChatAnthropic
        
        return ChatAnthropic
    

@llm_registry.register(ProviderType.GOOGLE)
class GoogleLLMStrategy(LLMStrategy):
    def _get_callable(self):
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        return ChatGoogleGenerativeAI
    

@llm_registry.register(ProviderType.MISTRAL)
class MistralAILLMStrategy(LLMStrategy):
    def _get_callable(self):
        from langchain_mistralai import ChatMistralAI
        
        return ChatMistralAI
    

@llm_registry.register(ProviderType.OLLAMA)
class OllamaLLMStrategy(LLMStrategy):
    def _get_callable(self):
        from langchain_ollama import ChatOllama
        
        return ChatOllama
    

@llm_registry.register(ProviderType.OPENAI)
class OpenAILLMStrategy(LLMStrategy):
    def _get_callable(self):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI
