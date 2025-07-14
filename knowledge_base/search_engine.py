import logging

logger = logging.getLogger(__name__)


class KnowledgeBaseSearchEngine:
    def __init__(self, index):
        self.index = index
        logger.info("KnowledgeBaseSearchEngine initialized.")

    def search(self, query: str, top_k: int = 1) -> list[dict]:
        try:
            if not query:
                raise ValueError("Query is empty.")
            logger.debug(f"Performing similarity search for query: {query}")
            results = self.index.similarity_search(query, k=top_k)
            if not results:
                logger.warning("No similarity results found.")
                return []
            return [
                {
                    "url": result.metadata.get("url"),
                    "title": result.metadata.get("title")
                } for result in results
            ]
        except Exception as e:
            logger.exception(f"Search failed: {e}")
            return []
