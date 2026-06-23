import re
from pathlib import Path
import polars as pl

from src.domain.service.data.informations.loaders.data_loader_strategy import DataLoaderStrategy
from src.domain.factories.components.data.informations.loaders.loaders import LoadersType
from src.domain.factories.components.data.informations.loaders.registry import data_loader_registry


@data_loader_registry.register(LoadersType.PDF)
class PDFLoaderStrategy(DataLoaderStrategy):
    def load(self, data_path: str, metadata_path: str = None) -> list:
        from langchain_community.document_loaders import PyPDFLoader

        documents = []
        path_obj = Path(data_path)
        
        metadata = self.metadata_loader(metadata_path)

        if not path_obj.exists():
            raise FileNotFoundError(f"Data directory not found: {data_path}")

        for pdf_file in path_obj.rglob('*.pdf'):
            loader = PyPDFLoader(str(pdf_file))
            pages = loader.load()
            
            doc_name = pdf_file.stem

            institution = "Unknown"
            category_rules = []

            if metadata is not None and not metadata.is_empty():
                df_pdf_file_name = metadata.filter(pl.col('doc_name') == doc_name)
                
                if not df_pdf_file_name.is_empty():
                    institution = df_pdf_file_name.select(pl.col('institution')).unique().item()
                    category_rules = (
                        df_pdf_file_name
                        .group_by('category')
                        .agg(pl.col('keyword'))
                        .to_dicts()
                    )

            compiled_rules = []
            for rule in category_rules:
                keywords_pattern = "|".join(re.escape(word.lower()) for word in rule['keyword'])
                regex_pattern = rf"\b({keywords_pattern})\b"
                compiled_rules.append({
                    "category": rule['category'],
                    "regex": re.compile(regex_pattern)
                })

            for page in pages:                        
                page.metadata["file_name"] = pdf_file.name
                page.metadata["institution"] = institution
                page.page_content = f"Content issued by {institution}.\n" + page.page_content

                found_categories = []
                text = page.page_content.lower()

                for rule in compiled_rules:
                    if rule["regex"].search(text):
                        found_categories.append(rule['category'])
                
                page.metadata["category"] = ", ".join(found_categories if found_categories else ["general"])
                        
            documents.extend(pages)
                    
        return documents
    