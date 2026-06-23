from src.domain.service.data.splitters.data_splitters_strategy import DataSplitterStrategy
from src.domain.factories.components.data.splitters.splitter import SplitterType
from src.domain.factories.components.data.splitters.registry import data_splitter_registry

@data_splitter_registry.register(SplitterType.RECURSIVE_CHARACTER)
class RecursiveCharacterSplitterStrategy(DataSplitterStrategy):
    def split(self, documents: list, chunk_size: int, chunk_overlap: int = 0) -> list:
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        chunks = text_splitter.split_documents(documents)
        return chunks