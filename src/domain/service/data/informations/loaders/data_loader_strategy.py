from abc import ABC, abstractmethod
from pathlib import Path

import polars as pl
import yaml


class DataLoaderStrategy(ABC):
    @abstractmethod
    def load(self, data_path: str, metadata_path: str = None):
        pass

    @staticmethod
    def metadata_loader(metadata_path: str = None) -> None | pl.DataFrame:
        if not metadata_path or not Path(metadata_path).exists():
            return
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            docs_data = data.get('documents', [])

            linhas_yaml = []  
            for doc in docs_data:
                doc_name = doc['name']
                institution = doc['institution']
                
                for category, content in doc['categories'].items():
                    for keyword in content['keywords']:
                        linhas_yaml.append({
                            "doc_name": doc_name,
                            "institution": institution,
                            "category": category,
                            "keyword": keyword
                        })
            
            df = pl.DataFrame(linhas_yaml)
            
            return df

        except yaml.YAMLError as exc:
            print(f"Error: {exc}")

        

        
