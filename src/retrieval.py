import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
import numpy as np
from pymongo import MongoClient

# Download NLTK data (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

# MongoDB connection details
MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_DB = "thesis"
MONGODB_COLLECTION_NODES = "gemini-graph-embedding-nodes"
MONGODB_COLLECTION_EDGES = "gemini-graph-embedding-edges"

# Load the SentenceTransformer model
print("Loading model...")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
print("Finished Loading model...")


def clean_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Remove stopwords and non-alphanumeric tokens
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    # Return the cleaned text
    return ' '.join(filtered_tokens)


def vector_search(query, collection_name, top_k=5):
    # Clean the query
    cleaned_query = clean_text(query)
    # Embed the query
    query_embedding = model.encode(cleaned_query)

    # Connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    collection = db[collection_name]

    # Retrieve all embeddings from the collection
    embeddings = []
    ids = []
    cursor = collection.find({})
    for doc in cursor:
        embeddings.append(doc['embedding'])
        ids.append(doc['id'])
    embeddings = np.array(embeddings)

    # Normalize embeddings
    embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    query_embedding_norm = query_embedding / np.linalg.norm(query_embedding)

    # Compute cosine similarities
    similarities = np.dot(embeddings_norm, query_embedding_norm)

    # Get the top K matches
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]
    top_k_ids = [ids[i] for i in top_k_indices]
    top_k_scores = [similarities[i] for i in top_k_indices]

    # Close the connection
    client.close()

    # Return the results
    return list(zip(top_k_ids, top_k_scores))


def main():
    query = "What is an ETF and how can I use it to build wealth?"
    top_k = 5
    print("\nTop {} matches in Nodes collection:".format(top_k))
    top_k_nodes = vector_search(query, MONGODB_COLLECTION_NODES, top_k=top_k)
    for idx, (node_id, score) in enumerate(top_k_nodes):
        print("Rank {}: Node ID {}, Similarity Score {:.4f}".format(idx + 1, node_id, score))

    print("\nTop {} matches in Edges collection:".format(top_k))
    top_k_edges = vector_search(query, MONGODB_COLLECTION_EDGES, top_k=top_k)
    for idx, (edge_id, score) in enumerate(top_k_edges):
        print("Rank {}: Edge ID {}, Similarity Score {:.4f}".format(idx + 1, edge_id, score))


if __name__ == "__main__":
    main()
