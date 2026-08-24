from enum import StrEnum, auto


class EnginesTypes(StrEnum):
    CHROMA = auto()
    QDRANT = auto()
    PGVECTOR = auto()
    PINECONE = auto()

