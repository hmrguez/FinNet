from newspaper import Article
import os
import json
from neo4j import GraphDatabase
import google.generativeai as genai
import re

from src.constants import BATCH_1_URLS

# Placeholder for Gemini API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)


def scrape_article(url):
    """
    Scrape the article from the given URL and return its text content.
    """
    article = Article(url)
    article.download()
    article.parse()
    return article.text


def summarize_text_with_gemini(text, all_entities):
    """
    Send the text to the Gemini API to get entities and relationships in JSON format.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        "Extract the main entities and relationships from this article, keep both entities and relationships simple. If text explicit, add any possible relationship between already existing entities and new ones in this article. Return the output as a JSON array of objects with 'subject', 'relationship', and 'object' properties: " + text + "\n Existing entities: " + str(
            all_entities))

    text = response.text.replace("```json", "").replace("```", "")

    return text  # Should be a JSON string


def parse_gemini_output(json_text):
    """
    Parse the JSON output from Gemini and extract entities and relationships.
    """
    try:
        data = json.loads(json_text)
        relationships = []
        entities = set()

        for item in data:
            subj = item.get('subject')
            rel = item.get('relationship')
            obj = item.get('object')
            if subj and rel and obj:
                relationships.append((subj, rel, obj))
                entities.update([subj, obj])
        return entities, relationships
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return set(), []


def normalize_entity_name(name):
    return name.strip().lower()


def sanitize_relationship_type(rel):
    # Replace non-alphanumeric characters with underscores
    rel_type = re.sub(r'\W+', '_', rel).upper()
    # Remove leading digits
    rel_type = re.sub(r'^\d+', '', rel_type)
    # Ensure it's not empty
    if not rel_type:
        rel_type = "REL"
    return rel_type


def build_graph_in_neo4j(entities, relationships):
    """
    Build a graph database in Neo4j with the extracted entities and relationships.
    """
    uri = "bolt://localhost:7687"  # Update with your Neo4j URI
    user = os.getenv("NEO4J_USER")  # Update with your Neo4j username
    password = os.getenv("NEO4J_PASSWORD")  # Update with your Neo4j password

    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        # Create nodes
        for entity in entities:
            session.run("MERGE (e:Entity {name: $name})", name=normalize_entity_name(entity))

        # Create relationships
        for subj, rel, obj in relationships:
            rel_type = sanitize_relationship_type(rel)
            query = """
                MATCH (a:Entity {name: $subj})
                MATCH (b:Entity {name: $obj})
                MERGE (a)-[r:%s]->(b)
            """ % rel_type
            session.run(query, subj=normalize_entity_name(subj), obj=normalize_entity_name(obj))
    driver.close()


def main(urls):
    all_entities = set()
    all_relationships = []

    for idx, url in enumerate(urls):
        # print(f"Processing article {idx + 1}/{len(urls)}: {url}")
        #
        # # Step 1: Scrape the article
        # print("Scraping the article...")
        # text = scrape_article(url)
        #
        # # Step 2: Write the text to a file
        # print("Writing the article text to file...")
        # with open(f"data/scrapped/article_text_{idx + 1}.txt", "w") as file:
        #     file.write(text)
        #
        # # Step 3: Summarize the text using the Gemini API
        # print("Summarizing the article...")
        # summary = summarize_text_with_gemini(text, all_entities)
        #
        # # Write the summary to a file
        # print("Writing the summary to file...")
        # with open(f"data/gemini-raw/article_summary_{idx + 1}.txt", "w") as file:
        #     file.write(summary)

        with open(f"data/gemini-raw/article_summary_{idx + 1}.txt", "r") as file:
            summary = file.read()

        # Step 4: Parse the JSON output to get entities and relationships
        print("Parsing the Gemini output...")
        entities, relationships = parse_gemini_output(summary)

        print("Entities: ", entities)
        print("Relationships: ", relationships)

        # Add entities to the global set
        all_entities.update(entities)

        # Add relationships, taking into account the existing entities
        all_relationships.extend(relationships)

    # After processing all articles, build the graph
    print("Building the graph database...")
    build_graph_in_neo4j(all_entities, all_relationships)

    print("Process completed successfully.")


if __name__ == '__main__':
    article_urls = BATCH_1_URLS
    main(article_urls)
