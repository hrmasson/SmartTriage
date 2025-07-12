from knowledge_base.service import KnowledgeBaseService
from orchestrator.dtos import Problem
from config.api_config import settings


def search():
    print("searching...")
    service = KnowledgeBaseService(dataset_path=settings.KNOWLEDGE_BASE_DATASET_PATH)
    problem = Problem(problem="I didn't receive my salary", category="HR")
    problem = Problem(problem="-- ----- ", category="---")
    result = service.find_solution(problem)
    print(result)

if __name__ == "__main__":
    search()