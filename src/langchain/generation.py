import torch.nn as nn
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)


class AnswerGenerator(nn.Module):
    def __init__(self, gemini_model_name, expert):
        super(AnswerGenerator, self).__init__()
        self.gemini_model = genai.GenerativeModel(gemini_model_name)
        self.expert = expert

    def forward(self, subgraph: dict, query: str, orchestrator: bool = False):
        textualized_graph = self.textualize(subgraph)
        combined_input = f"{textualized_graph} {query}"

        if orchestrator:
            prompt = f"These are the answers from several experts regarding this query: {query}. You are a finance expert. Formulate a well-defined and concise answer (no introduction) by combining all these expert answers: {combined_input}"
        else:
            prompt = f"You are an expert in the field of {self.expert}. Generate an answer with your point of view based on the following input: {combined_input}"

        response = self.gemini_model.generate_content(prompt)

        return response.text

    def textualize(self, subgraph):
        node_texts = [str(node) for node in subgraph['nodes']]
        edge_texts = [str(edge) for edge in subgraph['edges']]
        return " ".join(node_texts + edge_texts)

    @staticmethod
    def instance(expert):
        return AnswerGenerator(
            gemini_model_name='gemini-1.5-flash',
            expert=expert
        )
