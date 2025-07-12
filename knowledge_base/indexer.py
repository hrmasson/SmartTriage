import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from config.api_config import settings

class KnowledgeBaseIndexer:
    def __init__(self, embedding_model=None):
        self.embedding_model = embedding_model or HuggingFaceEmbeddings(
            model_name=settings.KNOWLEDGE_BASE_MODEL_NAME,
        )

    def build_index(self, data: list[dict]) -> FAISS:
       documents = [
           Document(
               page_content=item['text'],
               metadata={"title":item['title'], "url": item['url']}
           ) for item in data
       ]

       return FAISS.from_documents(documents, self.embedding_model)

    def save_index(self, index: FAISS, index_path: str):
        if not os.path.exists(os.path.dirname(index_path)):
            os.makedirs(os.path.dirname(index_path))
        index.save_local(index_path)

    def load_index(self, index_path: str):
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file {index_path} does not exist.")
        return FAISS.load_local(index_path, self.embedding_model, allow_dangerous_deserialization=True)
