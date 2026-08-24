import inspect

from langchain_core.tools import BaseTool, tool

from src.application.builder.agent.agent_product import AgentProduct
from src.domain.factories.base.registry import BaseRegistry

tool_register = BaseRegistry(registry_name="Tool Register")

@tool_register.register("retriever")
def create_retriever_tool(retriever):
    # @tool(args_schema=RetrieverInputModel)
    @tool
    def retriever_tool(query: str) -> str:
        """
        Use this tool to search information through the provided data documents.
        
        Args:
            query: The search string containing key terms. Must be a plain string.
        """
        docs = retriever.invoke(query)

        if not docs:
            return 'I found no relevant information in the documents.'
        
        results = [doc.page_content for doc in docs]
        return "\n\n".join(results)

    return retriever_tool

def prepare_agent_tools_list(agent: AgentProduct) -> list:
    agent_tools = []

    for name, item in tool_register.registries.items():
        if isinstance(item, BaseTool):
            agent_tools.append(item)
        
        elif callable(item):
            expected_parameters = inspect.signature(item).parameters
            kwargs_to_inject = {}
            can_instanciate = True

            for param_name in expected_parameters:
                if hasattr(agent, param_name) and getattr(agent, param_name) is not None:
                    kwargs_to_inject[param_name] = getattr(agent, param_name)
                else:
                    print(f"Tool '{name}' ignored: dependency '{param_name}' not found in the Agent")
                    can_instanciate = False
                    break 

            if can_instanciate:
                tool_ok = item(**kwargs_to_inject)
                agent_tools.append(tool_ok)
    
    return agent_tools
