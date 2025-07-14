import logging

from config.api_config import settings
from dispatcher.service import DispatcherService
from knowledge_base.service import KnowledgeBaseService
from llm.service import LlmService
from orchestrator.main_service import MainService
from rabbit.consumer import Consumer
from rabbit.producer import Producer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("smarttriage.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting SmartTriage service...")

    base_url = f"{settings.LOCALAI_BASE_URL}:{settings.LOCALAI_PORT}"

    logger.info(f"Using LLM at {base_url}")
    llm_service = LlmService(base_url=base_url, model_name=settings.LOCALAI_MODEL_NAME)
    dispatcher_service = DispatcherService(model_path=settings.DISPATCHER_MODEL_PATH,
                                           labels_path=settings.DISPATCHER_LABELS_PATH)
    knowledge_base_service = KnowledgeBaseService(dataset_path=settings.KNOWLEDGE_BASE_DATASET_PATH,
                                                  index_path=settings.KNOWLEDGE_BASE_INDEX_PATH)
    producer = Producer(queue_name=settings.RABBIT_OUTPUT_QUEUE)

    main_service = MainService(llm=llm_service,
                               dispatcher=dispatcher_service,
                               kb=knowledge_base_service,
                               producer=producer)
    consumer = Consumer(queue_name=settings.RABBIT_INPUT_QUEUE, on_message=main_service.handle_message)
    logger.info(f"Consumer is now listening on queue: {settings.RABBIT_INPUT_QUEUE}")
    consumer.consume()
