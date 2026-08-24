from langgraph.graph import StateGraph, END

from src.application.builder.agent.agent_product import AgentProduct
from src.application.builder.graph.base import Builder

from src.application.graph.nodes import call_llm, exists_action, take_action
from src.application.graph.state import AgentState
from src.application.graph.tools import prepare_agent_tools_list


class GraphBuilder(Builder):
    def set_pipeline(self, agent: AgentProduct, prompts: dict) -> StateGraph:
        agent_tools = prepare_agent_tools_list(agent=agent)
        
        agent_tools_dict = {t.name: t for t in agent_tools}
        
        llm = agent.llm
        if agent_tools:
            llm = llm.bind_tools(agent_tools)

        graph = StateGraph(AgentState)

        graph.add_node(
            'llm',
            lambda state: call_llm(
                state=state,
                llm=llm,
                system_prompt=prompts['system']
            )
        )

        graph.add_node(
            "action", 
            lambda state: take_action(
                state=state, 
                registred_tools=agent_tools_dict
            )
        )

        graph.add_conditional_edges(
            "llm",
            exists_action,
            {True: "action", False: END}
        )

        graph.add_edge("action", "llm")
        graph.set_entry_point('llm')

        return graph
