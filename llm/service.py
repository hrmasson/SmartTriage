from llm.localai import LocalAIClient
from orchestrator.dtos import Problem


class LlmService:
    def __init__(self, model_name: str, base_url: str):
        self.localai_client = LocalAIClient(base_url=base_url, model=model_name)

    def extract_problem_and_category(self, text: str) -> Problem:
        return self.localai_client.extract_problem_and_category(text)
