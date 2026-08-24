# src/application/services/ingestion_service.py
from tqdm import tqdm

from src.application.builder.agent.agent_builder import AgentBuilder
from src.domain.factories.components.vector_store.factory import (
    StrategyVectorStoreFactory,
)
from src.domain.models.agent_model import AgentModel


class IngestionService:
    @staticmethod
    def populate_vector_store(config_model: AgentModel, force_reset: bool = False, force_ingest: bool = False) -> None:
        if not force_reset and not force_ingest:
            return

        if force_reset and config_model.vector_store:
            engine = config_model.vector_store.engine
            resolved_path = f"./{config_model.vector_store.connection_path}_{config_model.vector_store.collection_name}"
            
            strategy_factory = StrategyVectorStoreFactory.execute(instance_type=engine)
            strategy_factory.reset_database(resolved_path)

        builder = AgentBuilder(config=config_model)
        builder.set_embeddings_model()
        builder.set_vector_store()
        builder.set_data()

        agent = builder.agent
        chunks = agent.data
        vector_store = agent.vector_store

        if not chunks:
            print("[Ingestion] No documents found to process.")
            return

        if not vector_store:
            raise RuntimeError(
                "Cannot ingest documents: 'vector_store' is not configured for this agent."
            )

        new_chunks = chunks
        if not force_reset:
            try:
                existing_docs = vector_store.get()
                if existing_docs and 'metadatas' in existing_docs and existing_docs['metadatas']:
                    indexed_files = {meta.get('filename') for meta in existing_docs['metadatas'] if meta and 'filename' in meta}
                    new_chunks = [c for c in chunks if c.metadata.get('filename') not in indexed_files]
            except Exception as e:
                print(f"[Ingestion] Could not read existing chunks: {e}")

        if not new_chunks:
            print("[Ingestion] All documents are already up to date.")
            return

        batch_size = config_model.vector_store.batch_size
        print(f"[Ingestion] Saving {len(new_chunks)} chunks to Vector Store...\n")

        for i in tqdm(range(0, len(new_chunks), batch_size)):
            batch = new_chunks[i:i + batch_size]
            vector_store.add_documents(batch)

        print("\n[Ingestion] Vector Store populated successfully!")