import uuid

from src.domain.factories.components.checkpointer.factory import StrategyCheckpointersFactory
from src.application.builder.graph.graph_builder import GraphBuilder
from src.application.builder.agent.agent_product import AgentProduct

class GraphFacade:
    
    @staticmethod
    def run_graph(
        agent: AgentProduct, 
        prompts: dict, 
        user_input: str, 
        session_id: str = None
    ) -> tuple[dict, str]:
        
        builder = GraphBuilder()
        graph = builder.set_pipeline(agent=agent, prompts=prompts)

        config = agent.checkpointer
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if not config:
            app = graph.compile()
            return app.invoke({"messages": [user_input]}), session_id
        
        saver = config.pop('saver')

        strategy = StrategyCheckpointersFactory.execute(saver)
        
        with strategy.start(**config) as checkpointer:
            app = graph.compile(checkpointer=checkpointer)
            
            response = app.invoke(
                {"messages": [user_input]}, 
                config={"configurable": {"thread_id": session_id}}
            )
            
            return response, session_id