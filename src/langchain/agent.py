import os

from langchain_core.messages import HumanMessage
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent
from neo4j import GraphDatabase

import networkx as nx
import google.generativeai as genai

from src.langchain.vector_search import vector_search

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

NEO4J_URI = "bolt://localhost:7687"  # Update if your Neo4j URI is different
NEO4J_USER = os.getenv("NEO4J_USER")  # Update with your Neo4j username
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # Update with your Neo4j password


# Step 1: Initialize Graph and Retrieval Logic
class GraphRAG:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.populate_graph()

    def populate_graph(self):
        # Neo4j connection details
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            # Fetch nodes
            nodes = session.run("MATCH (n) RETURN id(n) as id, n.name as name")
            for record in nodes:
                node_id = record["id"]
                name = record["name"]
                self.graph.add_node(node_id, description=name)

            # Fetch edges
            edges = session.run(
                "MATCH (n)-[r]->(m) RETURN id(r) as id, type(r) as type, n.id as source, m.id as target, r.name as name")
            for record in edges:
                edge_id = record["id"]
                edge_type = record["type"]
                source = record["source"]
                target = record["target"]
                name = record["name"] if record["name"] else edge_type
                self.graph.add_edge(source, target, description=name)

        driver.close()

    def retrieve_subgraph(self, query):
        # Retrieve relevant nodes for the query
        # Implement custom logic, e.g., BFS or content filtering
        relevant_nodes = list(nx.neighbors(self.graph, "Node A"))
        subgraph = self.graph.subgraph(relevant_nodes)
        return subgraph


class GraphQueryTool:
    def __init__(self, graph, vector_search_func):
        self.graph = graph
        self.vector_search = vector_search_func

    def __call__(self, query):
        """Queries the subgraph and returns relevant information."""
        matched_ids = self.vector_search(query)
        subgraph = self.graph.subgraph(matched_ids)

        # Extract information from the subgraph.  Adapt this based on your graph's data.
        nodes_data = [subgraph.nodes[node] for node in subgraph.nodes]
        edges_data = [subgraph[u][v] for u, v in subgraph.edges]

        # Format the data for the LLM.  Experiment with different formats.
        subgraph_info = {
            "nodes": nodes_data,
            "edges": edges_data
        }

        return str(subgraph_info)


graph_rag = GraphRAG()
graph_query_tool = GraphQueryTool(graph_rag.graph, vector_search)

model = ChatVertexAI(model="gemini-1.5-flash")

tools = [graph_query_tool]

agent_executor = create_react_agent(model, tools)

config = {"configurable": {"thread_id": "your_thread_id"}}  # Change thread ID for new conversations

query = "How are EFT and investors related?"
for chunk in agent_executor.stream({"messages": [HumanMessage(content=query)]}, config):
    print(chunk)
    print("----")

# Example of how to access just the agent's final response:
response = agent_executor.invoke({"messages": [HumanMessage(content=query)]}, config)
final_answer = response['messages'][-1].content  # Get the last message content
print(f"Final Answer: {final_answer}")