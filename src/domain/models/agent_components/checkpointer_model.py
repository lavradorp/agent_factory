from pydantic import BaseModel, Field, model_validator

from src.domain.factories.components.checkpointer.savers import SaverType

class CheckpointerModel(BaseModel):
    saver: SaverType
    environment: str = Field(pattern="^(local|cloud)$")
    connection_path: str | None = Field(default=None)

    @model_validator(mode="after")
    def validate_connection_path(self):
        if self.saver == SaverType.IN_MEMORY:
            self.connection_path = None
            return self
        
        if not self.connection_path or not self.connection_path.strip():
            raise ValueError(
                f"The field 'connection_path' is required when saver is '{self.saver.value}'."
            )
        
        return self