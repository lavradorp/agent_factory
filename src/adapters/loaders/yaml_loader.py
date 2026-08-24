import yaml


class YAMLLoader:
    @staticmethod
    def load(file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_dict = yaml.safe_load(file)
        
        return raw_dict