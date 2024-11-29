import torch
import torch.nn as nn
from neo4j.graph import Node
from torch_geometric.nn import GATConv, global_mean_pool
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)


class GraphEncoder(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(GraphEncoder, self).__init__()
        self.gat = GATConv(in_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.gat(x, edge_index)
        return x


class ProjectionLayer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super(ProjectionLayer, self).__init__()
        self.mlp = nn.Sequential(
            nn.Linear(in_dim, out_dim),
            nn.ReLU(),
            nn.Linear(out_dim, out_dim)
        )

    def forward(self, x):
        return self.mlp(x)


class TextEmbedder(nn.Module):
    def __init__(self, model_name):
        super(TextEmbedder, self).__init__()
        self.text_embedder = SentenceTransformer(model_name)

    def forward(self, text):
        return self.text_embedder.encode(text, convert_to_tensor=True)


class AnswerGenerator(nn.Module):
    def __init__(self, graph_encoder, projection_layer, text_embedder, gemini_model_name):
        super(AnswerGenerator, self).__init__()
        self.graph_encoder = graph_encoder
        self.projection_layer = projection_layer
        self.text_embedder = text_embedder
        self.gemini_model = genai.GenerativeModel(gemini_model_name)

    def forward(self, subgraph, query):
        nodes: [Node] = subgraph['nodes']
        edges = subgraph['edges']

        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

        # Extract node names and convert them to embeddings
        node_names = [node._properties['name'] for node in nodes]
        # x = self.m(node_names, convert_to_tensor=True)
        # Generate embeddings
        embeddings = model.encode(node_names)  # This returns a NumPy array

        # # Convert embeddings to a PyTorch tensor
        # x = torch.tensor(embeddings, dtype=torch.float32)
        #
        # x = x.view(-1, 128)  # Adjust the dimensions as needed
        #
        # # Convert edges to the format expected by the graph encoder
        # if edges:
        #     edge_index = torch.tensor([[edge['start_node'], edge['end_node']] for edge in edges],
        #                               dtype=torch.long).t().contiguous()
        #     # Filter out invalid edges
        #     valid_mask = (edge_index[0] < x.size(0)) & (edge_index[1] < x.size(0))
        #     edge_index = edge_index[:, valid_mask]
        # else:
        #     edge_index = torch.empty((2, 0), dtype=torch.long)
        #
        # if edge_index.size(1) > 0:
        #     hg = self.graph_encoder(x, edge_index)
        #     hg = global_mean_pool(hg, torch.zeros(hg.size(0),
        #                                           dtype=torch.long))  # Assuming all nodes belong to the same graph
        #     hg = self.projection_layer(hg)
        # else:
        #     hg = torch.zeros((x.size(0), 256))  # Adjust the size as needed

        textualized_graph = self.textualize(subgraph)
        combined_input = f"{textualized_graph} {query}"
        # ht = self.text_embedder(combined_input)

        response = self.gemini_model.generate_content(
            f"Generate an answer based on the following input: {combined_input}"
        )
        return response.text

    def textualize(self, subgraph):
        node_texts = []
        edge_texts = []

        for node in subgraph['nodes']:
            node_text = f"Node(id={node.id}, properties={node})"
            node_texts.append(node_text)

        for edge in subgraph['edges']:
            # print("Edge: ", edge)
            edge_text = str(edge)
            edge_texts.append(edge_text)

        return " ".join(node_texts + edge_texts)

    @staticmethod
    def instance():
        graph_encoder = GraphEncoder(in_channels=128, out_channels=256)
        projection_layer = ProjectionLayer(in_dim=256, out_dim=768)
        text_embedder = TextEmbedder(model_name='sentence-transformers/all-mpnet-base-v2')

        # Create the answer generator
        return AnswerGenerator(
            graph_encoder=graph_encoder,
            projection_layer=projection_layer,
            text_embedder=text_embedder,
            gemini_model_name='gemini-1.5-flash'
        )
