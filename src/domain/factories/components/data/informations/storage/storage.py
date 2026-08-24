from enum import StrEnum, auto


class StorageType(StrEnum):
    LOCAL = auto()
    S3 = auto()
