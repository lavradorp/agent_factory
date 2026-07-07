from src.domain.factories.components.retriever.registry import retriever_registry
from src.domain.factories.components.retriever.search_type import SearchType
from src.domain.service.retriever.retriever_strategy import RetrieverStrategy


@retriever_registry.register(
    SearchType.SIMILARITY,
    SearchType.SIMILARITY_SCORE_THRESHOLD,
    SearchType.MMR
)
class StandardRetrieverStrategy(RetrieverStrategy):
    def create(self, vectorstore, **kwargs):
        search_type = kwargs["search_type"]
        
        search_kwargs = {
            "k": kwargs["top_k"],
            # "tool_name": kwargs["tool_name"],
            # "description": kwargs["description"]
            }
        
        if search_type == "similarity_score_threshold":
            search_kwargs["score_threshold"] = kwargs["score_threshold"]

        retriever = vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )

        return retriever
    
