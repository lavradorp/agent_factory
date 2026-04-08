import yaml
import os

from pathlib import Path
from dotenv import load_dotenv

from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt

from .models.llm_config_model import LLMConfigModel


load_dotenv()
console = Console()

class LLMConfig:
    def __init__(self, config_path: str = "./config/yml"):
        self.config_path = Path(config_path)
        self.available_models: dict[str, LLMConfigModel] = {}
        self._load_config()

    def _load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration path not found: {self.config_path}")
        
        for yaml_file in self.config_path.glob("*.yml"):
            with open(yaml_file, "r", encoding="utf-8") as f:
                try:
                    config_data = yaml.safe_load(f)['llm']
                    validate_config = LLMConfigModel(**config_data)
                    self.available_models[yaml_file.name] = validate_config

                except Exception as e:
                    print(f"An error ocurred while loading {yaml_file.name}: {e}")                
    
    def select_model_cli(self) -> LLMConfigModel | None:
        if not self.available_models:
            console.print("No valid .yml files found in the config folder!")
            return None

        table = Table(title="🤖 Select the AI Engine", style="cyan")
        table.add_column("Option", justify="center", style="magenta", no_wrap=True)
        table.add_column("Provider", style="green")
        table.add_column("Model", style="yellow")
        table.add_column("Embedding", style="white")
        table.add_column("Type", style="white")
        table.add_column("URL", style="white")
  
        counter = 0
        for yaml_file, available_model in self.available_models.items():
            counter+=1
            table.add_row(
                str(counter),
                available_model.provider.capitalize(),
                available_model.model,
                available_model.embedding_model,
                available_model.type,
                available_model.base_url,
            )

        console.print(table)

        choice = IntPrompt.ask(
            "Select the desired option number",
            choices=[str(i) for i in range(1, len(self.available_models) + 1)],
            show_choices=False
        )
        models_list = list(self.available_models.values())
        selected_config = models_list[choice - 1]

        if selected_config.type == "cloud":
            env_var_name = selected_config.api_key
            if not os.getenv(env_var_name):
                console.print(f"\nError: Environment variable '{env_var_name}' not found in your .env file!")
                raise SystemExit("Please configure your .env file before proceeding.")
        
        console.print(f"\nStarting with {selected_config.provider.capitalize()} ({selected_config.model})...\n")

        return selected_config
    
    def initialize(self):
        llm_config = self.select_model_cli()

        provider = llm_config.provider
        llm_model = llm_config.model
        embedding_model = llm_config.embedding_model
        temperature = llm_config.temperature

        match provider:
            case "ollama":
                from langchain_ollama import ChatOllama, OllamaEmbeddings

                llm = ChatOllama(
                    model=llm_model,
                    temperature=temperature,
                    base_url=llm_config.base_url
                )
                
                embeddings = OllamaEmbeddings(
                    model=embedding_model,
                    base_url=llm_config.base_url
                )
            
            case "google":
                from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

                llm = ChatGoogleGenerativeAI(
                    model=llm_model,
                    temperature=temperature,
                )

                embeddings = GoogleGenerativeAIEmbeddings(
                    model=embedding_model,
                )

            case "openai":
                from langchain_openai import ChatOpenAI, OpenAIEmbeddings

                llm = ChatOpenAI(
                    model=llm_model,
                    temperature=temperature,
                )

                embeddings = OpenAIEmbeddings(
                    model=embedding_model,
                )
            
            case "mistral":
                from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings

                llm = ChatMistralAI(
                    model=llm_model,
                    temperature=temperature,
                )

                embeddings = MistralAIEmbeddings(
                    model=embedding_model,
                )

            case "anthropic":
                from langchain_anthropic import ChatAnthropic
                from langchain_huggingface import HuggingFaceEmbeddings

                llm = ChatAnthropic(
                    model=llm_model,
                    temperature=temperature,
                )

                embeddings = HuggingFaceEmbeddings(
                    model_name=embedding_model
                )
            
        return llm, embeddings
