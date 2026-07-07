class AgentProduct:
    def __init__(self):
        self.llm = None
        self.embeddings = None
        self.vector_store = None
        self.retriever = None
        self.data = []
        self.checkpointer = None