from enum import StrEnum, auto


class SaverType(StrEnum):
    SQLITE = auto()
    POSTGRES = auto()
    IN_MEMORY = auto()