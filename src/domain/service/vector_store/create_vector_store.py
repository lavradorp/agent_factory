from src.decorators.error_handling import error_handling
from src.domain.factories.components.vector_store.engines import EnginesTypes
from src.domain.factories.components.vector_store.registry import vector_store_registry
from src.domain.service.vector_store.vector_store_strategy import VectorStoreStrategy


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
            import os

            client = QdrantClient(url=kwargs['connection_path'],
                                   api_key=os.getenv('QDRANT_API_KEY'),
                                   prefer_grpc=True)
        else:
            raise ValueError(
                f"Invalid Qdrant 'type': '{vs_type}'. Expected 'memory', 'local' or 'cloud'."
            )

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


@vector_store_registry.register(EnginesTypes.PINECONE)
class PineconeVectorStoreStrategy(VectorStoreStrategy):
    @error_handling()
    def create(self, embeddings, **kwargs):
        import os

        from langchain_pinecone import PineconeVectorStore
        from pinecone import Pinecone, ServerlessSpec

        index_name = kwargs["collection_name"]

        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError(
                "Missing 'PINECONE_API_KEY' environment variable for the Pinecone vector store."
            )

        pc = Pinecone(api_key=api_key)

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=kwargs.get("dimension", 1024),
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=kwargs.get("cloud", "aws"),
                    region=kwargs.get("region", "us-east-1"),
                ),
            )

        return PineconeVectorStore(
            index=pc.Index(index_name),
            embedding=embeddings
        )

