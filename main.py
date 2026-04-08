import argparse
import os
from pathlib import Path
import sys

from src.ingestion.ingestion import DataIngestion
from src.llm_config import LLMConfig

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ingest', action='store_true', help='Ingest new documents without resetting')
    parser.add_argument('--reset', action='store_true', help='Reset the database and re-ingest all')
    args = parser.parse_args()
    
    llm_config = LLMConfig()
    llm, embeddings = llm_config.initialize()

    if not llm or not embeddings:
        print("\nSetup cancelled or failed. Exiting...")
        sys.exit(1)

    data_path = Path('./data')
    db_path = Path('./chroma_db')
    collection_name = "fin_comp"

    if args.reset and db_path.exists():
        import shutil
        print("Resetting database...\n")
        shutil.rmtree(db_path)

    db_exists = db_path.exists()

    if db_exists:
        db_exists = any(db_path.iterdir())

    if args.ingest or args.reset or not db_exists:
        print("Vector database not found or empty. Starting ingestion pipeline...")
        data_ingestion = DataIngestion(
            embeddings=embeddings, 
            data_path=data_path,
            db_path=db_path,
            collection_name=collection_name
        )
        data_ingestion.create_vectorstore()

if __name__ == '__main__':
    main()