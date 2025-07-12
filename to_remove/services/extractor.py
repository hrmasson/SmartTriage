from llm.localai import LocalAIClient
from typing import Dict


def extract():
    print("Extracting...")
    text = "Hi, I haven’t received my salary for this month yet. Could you please check if there was an issue with the payment? Thanks,"
    llm = LocalAIClient(base_url="http://localhost:8083", model="mistral")
    result = llm.extract_problem_and_category(text)
    print(result)

if __name__ == "__main__":
    extract()