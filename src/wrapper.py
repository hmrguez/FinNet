import torch
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os

# Load environment variables
from dotenv import load_dotenv

from src.answer_gen import AnswerGenerator

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)


class Wrapper:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password, gemini_model_name):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.answer_generator = AnswerGenerator.instance()
        self.gemini_model_name = gemini_model_name

    def retrieve_subgraph(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            nodes = []
            edges = []
            for record in result:
                nodes.append(record['n'])
                for rel in record['rels']:
                    edges.append({
                        'start_node': rel.start_node.id,
                        'end_node': rel.end_node.id,
                        'type': rel.type,
                        'properties': rel
                    })
            return {'nodes': nodes, 'edges': edges}

    def generate_answer(self, subgraph, query):
        return self.answer_generator(subgraph, query)

    def process_query(self, query):
        subgraph_query = "MATCH (n)-[r]->(m) RETURN n, collect(r) as rels LIMIT 10"  # Example query
        subgraph = self.retrieve_subgraph(subgraph_query)
        answer = self.generate_answer(subgraph, query)
        return answer


# Example usage
if __name__ == "__main__":
    wrapper = Wrapper(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user=os.getenv("NEO4J_USER"),
        neo4j_password=os.getenv("NEO4J_PASSWORD"),
        gemini_model_name='gemini-1.5-flash'
    )
    query = "How can I invest with low funds?"
    answer = wrapper.process_query(query)
    print(answer)
