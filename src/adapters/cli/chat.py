from rich.console import Console
from rich.prompt import Prompt
from src.application.facade.graph_facade import GraphFacade

class ChatCLI:
    def __init__(self):
        self.console = Console()
        self.graph_facade = GraphFacade()

    def run_conversation(self, agent, prompts: dict):
        self.console.print("\n[bold green]✅ Agent ready and connected![/bold green]")
        self.console.print("[italic gray](Type 'exit' or 'quit' to end the conversation)[/italic gray]")
        self.console.print("-" * 60)

        session_id = None

        while True:
            try:
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
                
                if user_input.lower().strip() in ['exit', 'quit']:
                    self.console.print("\n[bold yellow]👋 Ending chat. See you later![/bold yellow]")
                    break
                
                if not user_input.strip():
                    continue
                    
                with self.console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
                    response, session_id = self.graph_facade.run_graph(
                        agent=agent, 
                        prompts=prompts, 
                        user_input=user_input, 
                        session_id=session_id
                    )
                
                agent_message = response['messages'][-1].content
                self.console.print(f"[bold magenta]Agent:[/bold magenta] {agent_message}")
                self.console.print()
                
            except KeyboardInterrupt:
                self.console.print("\n\n[bold yellow]🛑 Chat interrupted (Ctrl+C).[/bold yellow]")
                break
            except Exception as e:
                self.console.print(f"\n[bold red]⚠️ Execution error:[/bold red] {e}")