from typing import List
from src.langchain.expert_agent import ExpertAgent, ExpertAgentText


class AgentOrchestrator:
    def __init__(self, expert_fields: List[str]):
        self.expert_fields = expert_fields
        self.agents = [ExpertAgent(expert_field) for expert_field in expert_fields]
        self.responses = []

    def call_agents(self, query: str):
        self.responses = [agent.expert_field + "expert: \n" + agent(query) for agent in self.agents]

    def generate_combined_answer(self, query: str) -> str:
        from src.langchain.generation import AnswerGenerator
        combined_input = " ".join(self.responses) + "\nQuery: " + query
        combined_expert = AnswerGenerator.instance("finance")
        return combined_expert({"nodes": [], "edges": []}, combined_input, orchestrator=True)

    def __call__(self, query: str) -> str:
        self.call_agents(query)
        return self.generate_combined_answer(query)


class AgentOrchestratorText:
    def __init__(self, expert_fields: List[str]):
        self.expert_fields = expert_fields
        self.agents = [ExpertAgentText(expert_field) for expert_field in expert_fields]
        self.responses = []

    def call_agents(self, query: str):
        self.responses = [agent.expert_field + "expert: \n" + agent(query) for agent in self.agents]

    def generate_combined_answer(self, query: str) -> str:
        from src.langchain.generation import AnswerGenerator
        combined_input = " ".join(self.responses) + "\nQuery: " + query
        combined_expert = AnswerGenerator.instance("finance")
        return combined_expert({"nodes": [], "edges": []}, combined_input, orchestrator=True)

    def __call__(self, query: str) -> str:
        self.call_agents(query)
        return self.generate_combined_answer(query)
