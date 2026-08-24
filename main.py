import argparse

from src.adapters.cli.agent_selector import AgentSelectorCLI
from src.adapters.cli.chat import ChatCLI
from src.adapters.loaders.yaml_loader import YAMLLoader

from src.domain.models.agent_model import AgentModel

from src.application.services.ingestion_service import IngestionService
from src.application.facade.agent_facade import AgentFacade
from src.application.facade.graph_facade import GraphFacade

def main():
    parser = argparse.ArgumentParser(description="Agent Factory Workflow CLI")
    parser.add_argument('--ingest', action='store_true', help='Ingest new documents without resetting')
    parser.add_argument('--reset', action='store_true', help='Reset the database and re-ingest all')
    parser.add_argument('--config', type=str, default=None, help='Path to YAML config')
    args = parser.parse_args()

    selector = AgentSelectorCLI()
    yaml_path = selector.select_model_cli()

    if yaml_path is None:
        return

    config = YAMLLoader.load(yaml_path)

    config_model = AgentModel(**config)

    IngestionService.populate_vector_store(
        config_model=config_model,
        force_reset=args.reset,
        force_ingest=(args.ingest or args.reset)
    )

    agent = AgentFacade.build_from_yaml(config_model)
  
    prompts = dict()

    with open(r'./config/markdown/system_prompt.md') as file:
        prompts['system'] = file.read()

        file.close()

    chat = ChatCLI()
    chat.run_conversation(agent=agent, prompts=prompts)

if __name__ == "__main__":
    main()