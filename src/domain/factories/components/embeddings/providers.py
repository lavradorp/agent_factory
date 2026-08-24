from enum import StrEnum, auto


class ProviderType(StrEnum):
    GENERIC = auto()
    GOOGLE = auto()
    HUGGING_FACE = auto()
    MISTRAL = auto()
    NOMIC = auto()
    OLLAMA = auto()
    OPENAI = auto()