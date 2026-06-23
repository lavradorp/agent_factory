from src.domain.factories.components.vector_store.registry import vector_store_registry
from src.domain.factories.components.vector_store.engines import EnginesTypes
from src.domain.service.vector_store.vector_store_strategy import VectorStoreStrategy
from src.decorators.error_handling import error_handling


@vector_store_registry.register(EnginesTypes.CHROMA)
class ChromaVectorStoreStrategy(VectorStoreStrategy):
    @error_handling()
    def create(self, embeddings, **kwargs):
        from langchain_chroma import Chroma

        collection_name = kwargs["collection_name"]
        connection_path = kwargs["connection_path"]

        db_path = f'./{connection_path}_{collection_name}'
        
        vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=db_path,
            collection_name=collection_name
        )

        return vector_store
    

@vector_store_registry.register(EnginesTypes.PGVECTOR)
class PGVectorStoreStrategy(VectorStoreStrategy):
    @error_handling()
    def create(self, embeddings, **kwargs):
        from langchain_postgres import PGVector

        collection_name = kwargs["collection_name"]
        connection_path = kwargs["connection_path"]

        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=connection_path,
            use_jsonb=True
        )

        return vector_store
    

@vector_store_registry.register(EnginesTypes.QDRANT)   
class QdrantVectorStoreStrategy(VectorStoreStrategy):
    @error_handling()
    def create(self, embeddings, **kwargs):
        from langchain_qdrant import QdrantVectorStore
        from qdrant_client import QdrantClient
        from qdrant_client.http.models import Distance, VectorParams

        collection_name = kwargs["collection_name"]
        vs_type = kwargs['type']

        if vs_type == 'memory':
            client = QdrantClient(':memory:')
        elif vs_type == 'local':
            client = QdrantClient(path=kwargs['connection_path'])
        elif vs_type == 'cloud':
            client = QdrantClient(url=kwargs['connection_path'],
                                   api_key=kwargs.get('api_key'), 
                                   prefer_grpc=True)

        if not client.collection_exists(collection_name=collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=kwargs.get('dimension', 1024),
                    distance=Distance.COSINE
                ),
            )

        return QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings
        )

