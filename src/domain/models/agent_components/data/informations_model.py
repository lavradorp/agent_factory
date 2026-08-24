
from pydantic import BaseModel, Field, model_validator

from src.domain.factories.components.data.informations.loaders.loaders import (
    LoadersType,
)
from src.domain.factories.components.data.informations.storage.storage import (
    StorageType,
)


class DataInformationsModel(BaseModel):
    data_storage: StorageType
    data_path: str
    data_loaders: LoadersType
    metadata_storage: StorageType | None = Field(default=None)
    metadata_path: str | None = Field(default=None)

    @model_validator(mode="after")
    def validate_meatdata(self):
        if self.metadata_path and not self.metadata_storage:
            raise ValueError("Metadata storage type is required when metadata path is defined.")
        return self
