from typing import Optional
from pydantic import BaseModel, Field, model_validator

from src.domain.factories.components.data.informations.storage.storage import StorageType
from src.domain.factories.components.data.informations.loaders.loaders import LoadersType


class DataInformationsModel(BaseModel):
    data_storage: StorageType
    data_path: str
    data_loaders: LoadersType
    metadata_storage: Optional[StorageType] = Field(default=None)
    metadata_path: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def validate_meatdata(self):
        if self.metadata_path and not self.metadata_storage:
            raise ValueError("Metadata storage type is required when metadata path is defined.")
        return self
