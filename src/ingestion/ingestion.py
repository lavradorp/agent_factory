import os
import logging
from pathlib import Path

logging.getLogger("pypdf").setLevel(logging.ERROR)

from tqdm import tqdm

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DataIngestion:
    def __init__(self, embeddings, data_path: Path, db_path: Path, collection_name: str):
        self.embeddings = embeddings
        self.data_path = data_path
        self.db_path = db_path
        self.collection_name = collection_name
        
    def _read_pdf_data(self) -> list:
        documents = []
        for subdir in self.data_path.iterdir():
            if subdir.is_dir():
                category = subdir.name.lower()

                for pdf_file in subdir.glob('*pdf'):
                    loader = PyPDFLoader(pdf_file)
                    pages = loader.load()

                    for page in pages:
                        page.metadata["category"] = category
                        page.metadata["filename"] = pdf_file.name

                    documents.extend(pages)
        
        return documents
    
    def chunks_generator(self):
        documents = self._read_pdf_data()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        chunks = text_splitter.split_documents(documents)

        return chunks

    def create_vectorstore(self):
        chunks = self.chunks_generator()

        if not chunks:
            print("\nNo documents found to process.")
            return

        vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory=str(self.db_path),
            collection_name=self.collection_name
        )

        existing_docs = vectorstore.get()

        indexed_files = {meta['filename'] for meta in existing_docs['metadatas']} if existing_docs['metadatas'] else set()

        new_chunks = [c for c in chunks if c.metadata['filename'] not in indexed_files]

        if not new_chunks:
            print("\nAll documents are already up to date. No new chunks added.")
            return

        batch_size = 100

        print(f"\nSaving {len(chunks)} chunks on Chroma in batches of {batch_size}...\n")

        for i in tqdm(range(0, len(chunks), batch_size)):
            batch = chunks[i:i + batch_size]
            vectorstore.add_documents(batch)
        
        print("\nVectorstore populated successfully!")