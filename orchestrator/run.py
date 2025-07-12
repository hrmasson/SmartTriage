from rabbit.consumer import Consumer
from orchestrator.main_service import MainService
from llm.service import LlmService
from knowledge_base.service import KnowledgeBaseService
from dispatcher.service import DispatcherService
from config.api_config import settings
from rabbit.producer import Producer

if __name__ == "__main__":
    base_url = f"{settings.LOCALAI_BASE_URL}:{settings.LOCALAI_PORT}"
    llm_service = LlmService( base_url=base_url, model_name=settings.LOCALAI_MODEL_NAME)
    dispatcher_service = DispatcherService(model_path = settings.DISPATCHER_MODEL_PATH, labels_path=settings.DISPATCHER_LABELS_PATH)
    knowledge_base_service = KnowledgeBaseService(dataset_path=settings.KNOWLEDGE_BASE_DATASET_PATH, index_path=settings.KNOWLEDGE_BASE_INDEX_PATH)
    producer = Producer(queue_name=settings.RABBIT_OUTPUT_QUEUE)

    main_service = MainService(llm=llm_service,
                               dispatcher=dispatcher_service,
                               kb=knowledge_base_service,
                               producer=producer)
    consumer = Consumer(queue_name=settings.RABBIT_INPUT_QUEUE, on_message=main_service.handle_message)
    consumer.consume()