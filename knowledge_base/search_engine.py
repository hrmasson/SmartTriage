class KnowledgeBaseSearchEngine:
    def __init__(self, index):
        self.index = index

    def search(self, query: str, top_k: int = 1) -> list[dict]:
        results = self.index.similarity_search(query, k=top_k)
        if not results:
            return []
        return [
            {
                "url": result.metadata.get("url"),
                "title": result.metadata.get("title")
            } for result in results
        ]
