import networkx as nx
from neo4j import GraphDatabase
from typing import List, Tuple, Dict, Any

import os
from dotenv import load_dotenv
from neo4j.graph import Node

load_dotenv()

NEO4J_URI = "bolt://localhost:7687"  # Update if your Neo4j URI is different
NEO4J_USER = os.getenv("NEO4J_USER")  # Update with your Neo4j username
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # Update with your Neo4j password


class SubgraphCreator:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.graph = nx.Graph()
        self._map_neo4j_to_networkx()

    def _map_neo4j_to_networkx(self) -> None:
        with self.driver.session() as session:
            result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m")

            for record in result:
                node1: Node = record["n"]
                node2 = record["m"]
                relationship = record["r"]
                relationship_type = relationship.type
                relationship_id = relationship.id

                self.graph.add_node(node1._properties['id'], **node1)
                self.graph.add_node(node2._properties['id'], **node2)
                self.graph.add_edge(node1._properties['id'], node2._properties['id'],
                                    id=relationship_id,
                                    type=relationship_type,
                                    source=node1._properties['id'],
                                    target=node2._properties['id'],
                                    **relationship)

    def get_subgraph(self, nodes: List[Tuple[str, float]], edges: List[Tuple[int, float]]) -> Dict[str, List[Any]]:
        node_ids = [node[0] for node in nodes]
        edge_ids = [edge[0] for edge in edges]

        subgraph_nodes = set(node_ids)
        subgraph_edges = set()

        for edge in edge_ids:
            for u, v, data in self.graph.edges(data=True):
                if data.get('id') == edge:
                    subgraph_edges.add((u, v))
                    subgraph_nodes.add(u)
                    subgraph_nodes.add(v)

        subgraph = self.graph.subgraph(subgraph_nodes).copy()

        return {
            "nodes": [self.graph.nodes[node] for node in subgraph.nodes],
            "edges": [self.graph.edges[edge] for edge in subgraph.edges]
        }
    
    def get_advanced_connected_subgraph(self, nodes: List[Tuple[str, float]], edges: List[Tuple[int, float]]) -> Dict[str, List[Any]]:
        node_ids = {node[0] for node in nodes}
        edge_ids = {edge[0] for edge in edges}
        
        subgraph_nodes = set(node_ids)
        subgraph_edges = set()
        
        for u, v, data in self.graph.edges(data=True):
            if data.get('id') in edge_ids:
                subgraph_edges.add((u, v))
                subgraph_nodes.add(u)
                subgraph_nodes.add(v)
        
        # Ensure connectivity by finding the minimum spanning tree over required nodes
        induced_subgraph = self.graph.subgraph(subgraph_nodes).copy()
        
        if not nx.is_connected(induced_subgraph):
            # Find shortest paths between all required nodes to enforce connectivity
            extra_edges = set()
            for n1, n2 in combinations(subgraph_nodes, 2):
                if nx.has_path(self.graph, n1, n2):
                    path = nx.shortest_path(self.graph, n1, n2)
                    for i in range(len(path) - 1):
                        extra_edges.add((path[i], path[i + 1]))
            
            subgraph_edges.update(extra_edges)
            subgraph_nodes.update({node for edge in extra_edges for node in edge})
        
        final_subgraph = self.graph.subgraph(subgraph_nodes).copy()
        
        return {
            "nodes": [self.graph.nodes[node] for node in final_subgraph.nodes],
            "edges": [self.graph.edges[edge] for edge in final_subgraph.edges]
        }
