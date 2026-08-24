import pytest
from pydantic import ValidationError

from src.domain.models.agent_components.checkpointer_model import CheckpointerModel


def test_in_memory_does_not_require_connection_path():
    model = CheckpointerModel(saver="in_memory", environment="local")
    assert model.connection_path is None


def test_sqlite_requires_connection_path():
    with pytest.raises(ValidationError):
        CheckpointerModel(saver="sqlite", environment="local")


def test_postgres_with_connection_path_is_valid():
    model = CheckpointerModel(
        saver="postgres",
        environment="local",
        connection_path="postgresql://user:pass@localhost:5432/db",
    )
    assert model.connection_path.startswith("postgresql://")
