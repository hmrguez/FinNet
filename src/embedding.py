import os

from neo4j import GraphDatabase
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np

from dotenv import load_dotenv
load_dotenv()

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"  # Update if your Neo4j URI is different
NEO4J_USER = os.getenv("NEO4J_USER")  # Update with your Neo4j username
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # Update with your Neo4j password

# MongoDB connection details
MONGODB_URI = "mongodb://localhost:27017/"  # Update if your MongoDB URI is different
MONGODB_DB = "thesis"
MONGODB_COLLECTION_NODES = "gemini-graph-embedding-nodes"
MONGODB_COLLECTION_EDGES = "gemini-graph-embedding-edges"

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Connect to MongoDB
mongo_client = MongoClient(MONGODB_URI)
mongo_db = mongo_client[MONGODB_DB]
mongo_collection_nodes = mongo_db[MONGODB_COLLECTION_NODES]
mongo_collection_edges = mongo_db[MONGODB_COLLECTION_EDGES]


def extract_and_embed():
    with driver.session() as session:
        # Extract nodes
        print("Extracting nodes...")
        nodes = session.run("MATCH (n) RETURN n.id as id")
        for record in nodes:
            print(record)
            node_id = record["id"]
            embedding = model.encode(node_id)
            doc = {
                "id": node_id,
                "embedding": embedding.tolist()
            }
            mongo_collection_nodes.insert_one(doc)

        # Extract edges
        print("Extracting edges...")
        edges = session.run("MATCH ()-[r]->() RETURN id(r) as id, type(r) as type, r.name as name")
        for record in edges:
            edge_id = record["id"]
            edge_type = record["type"]
            name = record["name"] if record["name"] else edge_type
            if name:
                embedding = model.encode(name)
                doc = {
                    "id": edge_id,
                    "embedding": embedding.tolist()
                }
                mongo_collection_edges.insert_one(doc)
            else:
                print(f"Edge {edge_id} does not have a 'name' or 'type' property.")


if __name__ == "__main__":
    extract_and_embed()
    print("Finished processing nodes and edges.")
    # Close the connections
    driver.close()
    mongo_client.close()
