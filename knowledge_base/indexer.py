import logging
import os

from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from config.api_config import settings

logger = logging.getLogger(__name__)


class KnowledgeBaseIndexer:
    def __init__(self, embedding_model=None):
        self.embedding_model = embedding_model or HuggingFaceEmbeddings(
            model_name=settings.KNOWLEDGE_BASE_MODEL_NAME,
        )
        logger.info("KnowledgeBaseIndexer initialized with embedding model.")

    def build_index(self, data: list[dict]) -> FAISS:
        try:
            documents = [
                Document(
                    page_content=item['text'],
                    metadata={"title": item['title'], "url": item['url']}
                ) for item in data
            ]
            logger.info(f"Building FAISS index from {len(documents)} documents.")
            return FAISS.from_documents(documents, self.embedding_model)
        except Exception as e:
            logger.exception(f"Failed to build index: {e}")
            raise

    def save_index(self, index: FAISS, index_path: str):
        try:
            if not os.path.exists(os.path.dirname(index_path)):
                os.makedirs(os.path.dirname(index_path))
            logger.info(f"Saving FAISS index to {index_path}")
            index.save_local(index_path)
        except Exception as e:
            logger.exception(f"Failed to save index: {e}")
            raise

    def load_index(self, index_path: str):
        try:
            if not os.path.exists(index_path):
                raise FileNotFoundError(f"Index file {index_path} does not exist.")
            logger.info(f"Loading FAISS index from {index_path}")
            return FAISS.load_local(index_path, self.embedding_model, allow_dangerous_deserialization=True)
        except Exception as e:
            logger.exception(f"Failed to load index: {e}")
            raise
