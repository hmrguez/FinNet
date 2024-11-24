import os
import sys

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

from dotenv import load_dotenv

load_dotenv()

# MongoDB connection details
MONGODB_URI = "mongodb://localhost:27017/"  # Update if your MongoDB URI is different
MONGODB_DB = "thesis"
MONGODB_COLLECTION_TEXT = "gemini-text-embedding"

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Connect to MongoDB
mongo_client = MongoClient(MONGODB_URI)
mongo_db = mongo_client[MONGODB_DB]
mongo_collection_text = mongo_db[MONGODB_COLLECTION_TEXT]

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')


def clean_text(text):
    # Remove non-alphanumeric characters
    text = re.sub(r'\W+', ' ', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Convert to lower case
    tokens = [token.lower() for token in tokens]
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # Rejoin tokens into a string
    cleaned_text = ' '.join(tokens)
    return cleaned_text


def process_and_embed(folder_path):
    file_id = 0
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_id += 1
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    cleaned_text = clean_text(text)
                    embedding = model.encode(cleaned_text)
                    doc = {
                        "id": file_id,
                        "filename": filename,
                        "embedding": embedding.tolist()
                    }
                    mongo_collection_text.insert_one(doc)
                    print(f"Processed and inserted embedding for {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <folder_path>")
    #     sys.exit(1)
    folder_path = "data/scrapped"
    process_and_embed(folder_path)
    print("Finished processing files.")
    # Close the connection
    mongo_client.close()
