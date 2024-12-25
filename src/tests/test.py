import os
import time
import json
from src.langchain.agent_orchestrator import AgentOrchestrator, AgentOrchestratorText
from src.langchain.vector_search import vector_search, search_graph
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
import google.generativeai as genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print(GEMINI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

queries = [
    # General Budgeting
    ("What percentage of my income should I allocate to savings according to the 50/30/20 rule?",
     "According to the 50/30/20 rule, 20% of your income should be allocated to savings."),
    ("If I save $200 monthly for 5 years with an annual interest rate of 4%, how much will I have?",
     "With monthly savings of $200 and a 4% annual interest rate, compounded monthly, you will have approximately $13,243 after 5 years."),
    ("What’s the best way to track my daily expenses without using a paid app?",
     "You can track your daily expenses using free tools like Excel, Google Sheets, or free mobile apps like Mint or Spendee."),

    # Savings and Investments
    ("Explain the difference between a high-yield savings account and a certificate of deposit (CD).",
     "A high-yield savings account offers liquidity and variable interest, while a CD locks your money for a fixed term at a higher fixed interest rate."),
    ("How can I calculate compound interest for my savings manually?",
     "Compound interest is calculated using the formula A = P(1 + r/n)^(nt), where A is the future value, P is the principal, r is the annual interest rate, n is the number of times interest is compounded per year, and t is the time in years."),
    ("What are the tax advantages of contributing to a Roth IRA compared to a Traditional IRA?",
     "Contributions to a Roth IRA are made with after-tax income, but withdrawals are tax-free. Contributions to a Traditional IRA are tax-deductible, but withdrawals are taxed."),

    # Debt Management
    ("How much should I pay monthly to clear a $5,000 loan in 2 years with a 5% annual interest rate?",
     "You should pay approximately $219.36 monthly to clear a $5,000 loan with a 5% interest rate over 2 years."),
    ("Is it better to pay off high-interest debt first or focus on smaller debts?",
     "Paying off high-interest debt first (avalanche method) saves more money on interest, but focusing on smaller debts (snowball method) can provide motivation through quick wins."),
    ("What’s the snowball method for paying off debt?",
     "The snowball method involves paying off your smallest debts first while making minimum payments on others, then rolling the freed-up money into the next smallest debt."),

    # Taxation
    ("What are the standard tax deductions I can claim as a single filer in the U.S.?",
     "For 2024, the standard deduction for a single filer is $13,850. Other deductions depend on specific qualifications, such as student loan interest or medical expenses."),
    ("How does the tax bracket system work for someone earning $60,000 annually?",
     "For a single filer, your income will be taxed progressively. For 2024, you’ll pay 10% on income up to $11,000, 12% on income from $11,001 to $44,725, and 22% on income above that."),
    ("What are the key differences between tax credits and tax deductions?",
     "Tax credits directly reduce the taxes you owe, while tax deductions lower your taxable income."),

    # Retirement Planning
    ("How much should I save annually to retire with $1,000,000 by age 65, assuming 7% annual returns?",
     "If you start at age 30 and aim for $1,000,000 with 7% annual returns, you need to save approximately $6,650 annually."),
    ("What’s the difference between a 401(k) and a Roth IRA for retirement savings?",
     "A 401(k) is employer-sponsored with pre-tax contributions, while a Roth IRA is individually managed with after-tax contributions and tax-free withdrawals."),
    ("How can I estimate the Social Security benefits I’ll receive at retirement?",
     "You can estimate Social Security benefits using the SSA's online calculator, based on your earnings history and planned retirement age."),

    # Expense Optimization
    ("What are some tips for reducing grocery expenses without sacrificing nutrition?",
     "Plan meals, buy in bulk, prioritize seasonal produce, and avoid processed foods to save on groceries while maintaining nutrition."),
    ("Is refinancing my mortgage a good idea if I’m getting a 1% lower interest rate?",
     "Refinancing could save money if the interest reduction outweighs closing costs and you plan to stay in the home long-term."),
    ("How can I cut costs on my utility bills without major lifestyle changes?",
     "You can lower utility bills by sealing drafts, using energy-efficient appliances, and setting your thermostat wisely."),

    # Emergency Funds
    ("How large should my emergency fund be if I spend $3,000 monthly on essentials?",
     "Your emergency fund should cover 3–6 months of expenses, totaling $9,000–$18,000."),
    ("What’s the best way to build an emergency fund quickly without taking on debt?",
     "Cut non-essential expenses, sell unused items, and redirect bonuses or tax refunds to your emergency fund."),

    # Robustness Testing (Intentional Errors)
    ("How much will I save monthly if I earn $4,000 but spend $6,000 each month?",
     "You cannot save monthly if your expenses exceed your income. You need to reduce spending or increase income."),
    ("What’s the 60/40/10 budgeting rule, and how should I apply it?",
     "There is no 60/40/10 rule in standard budgeting. Did you mean the 50/30/20 rule? If so, allocate 50% to needs, 30% to wants, and 20% to savings."),
    ("If I save $100 weekly for 2 years at a 10% interest rate, what will I have in 5 years?",
     "There is a mismatch in the timeframes. Can you clarify if you want the total after 2 or 5 years?"),
    ("How much should I save for retirement if I want $1,000,000 by age 60, and I’m 50 now?",
     "Saving $1,000,000 in 10 years may not be feasible without very high contributions. Consider consulting a financial planner for a realistic target."),
    ("Can I claim tax deductions for donations I made in cash without receipts?",
     "You generally need receipts or documentation to claim deductions for cash donations on your taxes.")
]

expert_fields = ["personal finance", "economics", "investment"]

if __name__ == "__main__":
    # temp = search_graph("How are EFT and investors related?", is_text=True)
    # print(temp)

    agent_orchestrator = AgentOrchestratorText(expert_fields)

    results = []

    for query, expected_answer in queries:

        while True:
            try:
                start_time = time.time()
                # gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
                # result = gemini_model.generate_content(query).text
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
                break
            except Exception as e:
                print(f"An error occurred: {e}. Retrying in 1 minute...")
                time.sleep(60)

    with open('results_rag_text.json', 'w') as f:
        json.dump(results, f, indent=4)
