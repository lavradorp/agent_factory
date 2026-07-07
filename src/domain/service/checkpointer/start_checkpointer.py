from contextlib import contextmanager
from pathlib import Path

from src.domain.service.checkpointer.checkpointer_strategy import CheckpointerStrategy
from src.domain.factories.components.checkpointer.savers import SaverType
from src.domain.factories.components.checkpointer.registry import checkpointer_registry


@checkpointer_registry.register(SaverType.IN_MEMORY)
class InMemoryCheckpointerStrategy(CheckpointerStrategy):
    @contextmanager
    def start(self, **kwargs):
        from langgraph.checkpoint.memory import InMemorySaver

        checkpointer = InMemorySaver()

        yield checkpointer


@checkpointer_registry.register(SaverType.SQLITE)
class SQLiteCheckpointerStrategy(CheckpointerStrategy):
    @contextmanager
    def start(self, **kwargs):
        from langgraph.checkpoint.sqlite import SqliteSaver
        import sqlite3

        connection_path = kwargs["connection_path"]
        
        Path(connection_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(connection_path, check_same_thread=False) as conn:
            checkpointer = SqliteSaver(conn)
            checkpointer.setup()
            
            yield checkpointer


@checkpointer_registry.register(SaverType.POSTGRES)
class PostgresCheckpointerStrategy(CheckpointerStrategy):
    @contextmanager
    def start(self, **kwargs):
        from langgraph.checkpoint.postgres import PostgresSaver
        from psycopg_pool import ConnectionPool

        connection_path = kwargs["connection_path"]
        
        with ConnectionPool(
            conninfo=connection_path,
            max_size=20,
            kwargs={"autocommit": True}
        ) as pool:

            checkpointer = PostgresSaver(pool)
            
            checkpointer.setup() 

            yield checkpointer
