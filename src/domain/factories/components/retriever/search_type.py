from enum import StrEnum, auto


class SearchType(StrEnum):
    SIMILARITY = auto()
    SIMILARITY_SCORE_THRESHOLD = auto()
    MMR = auto()