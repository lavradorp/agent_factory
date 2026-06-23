from enum import StrEnum, auto


class ProviderType(StrEnum):
    GENERIC = auto()
    ANTHROPIC = auto()
    GOOGLE = auto()
    MISTRAL = auto()
    OLLAMA = auto()
    OPENAI = auto()