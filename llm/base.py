from abc import ABC, abstractmethod
from orchestrator.dtos import Problem


class LLMClient(ABC):
    @abstractmethod
    def extract_problem_and_category(self, text: str) -> Problem:
        """Send text to LLM and extract problem and category."""
        ...
