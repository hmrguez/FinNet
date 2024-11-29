import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from answer_gen import AnswerGenerator

load_dotenv()

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def get_subgraph(node_ids):
    with driver.session() as session:
        # Create a Cypher query to extract the subgraph
        query = """
        MATCH (n)
        WHERE id(n) IN $node_ids
        OPTIONAL MATCH (n)-[r]->(m)
        WHERE id(m) IN $node_ids
        RETURN n, r, m
        """
        result = session.run(query, node_ids=node_ids)

        nodes = []
        edges = []
        for record in result:
            nodes.append(record['n'])
            if record['r']:
                edges.append(record['r'])

        return nodes, edges


if __name__ == "__main__":
    # Example usage
    node_ids = [1256, 1536, 2267, 3118, 2080]  # Replace with your retrieved node IDs
    nodes, edges = get_subgraph(node_ids)

    subgraph_data = {
        'nodes': nodes,
        'edges': edges
    }

    query = "What can I do for a low-cost investment?"  # Replace with your query

    # Generate the answer
    answer_generator = AnswerGenerator.instance()
    answer = answer_generator(subgraph_data, query)
    print(answer)