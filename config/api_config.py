from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
class Settings(BaseSettings):
    LOCALAI_BASE_URL: str = "http://localhost"
    LOCALAI_PORT: int = 8083
    LOCALAI_MODEL_NAME: str = "mistral"

    KNOWLEDGE_BASE_DATASET_PATH: str = "data/knowledge_base_dataset.json"
    KNOWLEDGE_BASE_INDEX_PATH: str = "models/indices/faq_index"
    KNOWLEDGE_BASE_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    DISPATCHER_PROBLEM_DATASET_PATH: str = "data/dispatcher_problem_dataset.json"
    DISPATCHER_MODEL_PATH: str = "models/dispatcher/model.pkl"
    DISPATCHER_LABELS_PATH: str = "models/dispatcher/labels.pkl"

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_USER: str = "rabbitmq"
    RABBITMQ_PASS: str =  "rabbitmq"
    RABBIT_INPUT_QUEUE: str = "input_queue"
    RABBIT_OUTPUT_QUEUE: str = "output_queue"



settings = Settings()