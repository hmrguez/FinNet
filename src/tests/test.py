import os
import time
import json
from src.langchain.agent_orchestrator import AgentOrchestrator
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
import google.generativeai as genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print(GEMINI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

queries = [
    ("How are investors related with EFT?", "Investors are related to ETFs as they can invest in them to diversify their portfolios.")
]

expert_fields = ["personal finance", "economics", "investment"]

if __name__ == "__main__":

    agent_orchestrator = AgentOrchestrator(expert_fields)

    results = []

    for query, expected_answer in queries:
        start_time = time.time()
        result = agent_orchestrator(query)
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Calculate BLEU score
        bleu_score = sentence_bleu([expected_answer.split()], result.split())

        # Calculate ROUGE score
        rouge = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
        rouge_scores = rouge.score(expected_answer, result)

        # Use Gemini API to assess the quality of the response
        gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        prompt = f"Assess the quality of the following response. Return the answer in json format with a property called rating which is the number:\n\nQuery: {query}\nResponse: {result}'"
        gemini_response = gemini_model.generate_content(prompt)
        gemini_score = gemini_response.text

        results.append({
            "query": query,
            "result": result,
            "expected_answer": expected_answer,
            "time_spent": elapsed_time,
            "bleu_score": bleu_score,
            "rouge_scores": rouge_scores,
            "gemini_score": gemini_score
        })

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)