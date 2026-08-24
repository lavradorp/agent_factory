from pathlib import Path

from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table

from src.adapters.loaders.yaml_loader import YAMLLoader


class AgentSelectorCLI:
    def __init__(self, config_path: str = "./config/yml/agents"):
        self.path = Path(config_path)
        self.console = Console()

    def _discover_yaml_configs(self) -> dict[int, Path]:
        if not self.path.exists():
            return {}
        
        yaml_files = list(self.path.glob("*.yml")) + list(self.path.glob("*.yaml"))
        return {index + 1: file_path for index, file_path in enumerate(yaml_files)}

    def select_model_cli(self) -> Path | None:
        try:
            available_files = self._discover_yaml_configs()

            if not available_files:
                self.console.print(f"[bold red]No valid .yml or .yaml files found in {self.path.resolve()}![/bold red]")
                return None

            table = Table(title="🤖 Available AI Agent Configurations", style="cyan")
            table.add_column("Option", justify="center", style="magenta", no_wrap=True)
            table.add_column("Config File", style="green")
            table.add_column("LLM Provider", style="yellow")
            table.add_column("LLM Model", style="white")
            table.add_column("Embedding Encoder", style="blue")

            for option_id, file_path in available_files.items():
                try:
                    
                    content = YAMLLoader.load(file_path)

                    llm_info = content.get("llm", {})
                    embedding_info = content.get("embeddings", {})

                    table.add_row(
                        str(option_id),
                        file_path.name,
                        str(llm_info.get("provider", "N/A")).capitalize(),
                        str(llm_info.get("model", "N/A")),
                        str(embedding_info.get("model", "No Embedding (Core Chat)")),
                    )
                except Exception:
                    table.add_row(str(option_id), file_path.name, "Error reading file", "-", "-")

            self.console.print(table)

            choice = IntPrompt.ask(
                "Select the desired option number",
                choices=[str(i) for i in available_files.keys()],
                show_choices=False
            )

            selected_path = available_files[choice]
            self.console.print(f"\n[bold green]Loaded configuration:[/bold green] {selected_path.name}\n")
            
            return selected_path
        
        except KeyboardInterrupt:
            self.console.print("\n\n[bold yellow]🛑 Chat interrupted (Ctrl+C).[/bold yellow]")
        except Exception as e:
            self.console.print(f"\n[bold red]⚠️ Execution error:[/bold red] {e}")