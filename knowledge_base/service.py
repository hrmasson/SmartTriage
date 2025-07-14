import json
import logging
import os

from knowledge_base.indexer import KnowledgeBaseIndexer
from knowledge_base.search_engine import KnowledgeBaseSearchEngine
from orchestrator.dtos import Problem, Solution

logger = logging.getLogger(__name__)


def load_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error: The file {file_path} is not a valid JSON file.")
        return None


def init_index(dataset_path: str, index_path: str):
    indexer = KnowledgeBaseIndexer()

    index_faiss = os.path.join(index_path, "index.faiss")
    index_pkl = os.path.join(index_path, "index.pkl")

    if index_path and os.path.isfile(index_faiss) and os.path.isfile(index_pkl):
        logger.info("Loading existing index from disk.")
        return indexer.load_index(index_path)
    elif dataset_path and os.path.exists(dataset_path):
        logger.info("Building new index from dataset.")
        data = load_file(dataset_path)
        if data is None:
            raise ValueError("Failed to load knowledge base data.")
        index = indexer.build_index(data)
        if index_path:
            indexer.save_index(index, index_path=index_path)
        return index
    else:
        raise ValueError("Either dataset_path or index_path must be provided and valid.")


class KnowledgeBaseService:
    def __init__(self, dataset_path: str = None, index_path: str = None):
        index = init_index(dataset_path, index_path)
        self.search_engine = KnowledgeBaseSearchEngine(index)
        logger.info("KnowledgeBaseService initialized.")

    def find_solution(self, problem: Problem, top_k: int) -> list[Solution]:
        try:
            if not problem or not problem.problem:
                raise ValueError("Problem text is empty or invalid.")
            logger.debug(f"Searching for solutions for: {problem.problem}")
            results = self.search_engine.search(problem.problem, top_k=top_k)
            return [
                Solution(title=result['title'], url=result['url'])
                for result in results
            ]
        except Exception as e:
            logger.exception(f"Failed to search knowledge base: {e}")
            return [Solution(title="Search failed", url="")]
