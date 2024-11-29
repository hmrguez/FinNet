from typing import Optional

from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_google_vertexai import ChatVertexAI
import google.generativeai as genai
import vertexai
from langchain_experimental.graph_transformers import LLMGraphTransformer
import asyncio
import nest_asyncio

import os
from dotenv import load_dotenv
from lazy_object_proxy.utils_py3 import await_

load_dotenv()

NEO4J_URI = "bolt://localhost:7687"  # Update if your Neo4j URI is different
NEO4J_USER = os.getenv("NEO4J_USER")  # Update with your Neo4j username
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # Update with your Neo4j password

graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USER,
    password=NEO4J_PASSWORD,
    refresh_schema=False
)

text = """
Marie Curie, 7 November 1867 – 4 July 1934, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
She was, in 1906, the first woman to become a professor at the University of Paris.
Also, Robin Williams!
"""
documents = [Document(page_content=text)]

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

vertexai.init(project="793371050233")

llm = ChatVertexAI(model_name='gemini-1.5-flash')

no_schema = LLMGraphTransformer(llm=llm)

nest_asyncio.apply()


async def main():
    data = await no_schema.aconvert_to_graph_documents(documents)
    return data


if __name__ == "__main__":
    # print(os.getenv('GOOGLE_APPLICATION_CREDENTIAL'))
    data = asyncio.get_event_loop().run_until_complete(main())

