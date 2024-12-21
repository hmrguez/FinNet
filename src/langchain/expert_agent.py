class ExpertAgent:
    def __init__(self, expert_field: str):
        self.expert_field = expert_field
        self.nodes = None
        self.edges = None
        self.subgraph_data = None
        self.answer = None

    def search_graph(self):
        from src.langchain.vector_search import search_graph
        self.nodes, self.edges = search_graph(self.query)

    def create_subgraph(self):
        from src.langchain.subgraph import SubgraphCreator
        subgraph_creator = SubgraphCreator()
        self.subgraph_data = subgraph_creator.get_subgraph(self.nodes, self.edges)

    def generate_answer(self):
        from src.langchain.generation import AnswerGenerator
        financial_expert = AnswerGenerator.instance(self.expert_field)
        self.answer = financial_expert(self.subgraph_data, self.query)

    def __call__(self, query: str, *args, **kwargs):
        self.query = query
        self.search_graph()
        self.create_subgraph()
        self.generate_answer()
        return self.answer
