import logging
from concurrent.futures import ThreadPoolExecutor

from dispatcher.service import DispatcherService
from knowledge_base.service import KnowledgeBaseService
from llm.service import LlmService
from orchestrator.dtos import Solution
from rabbit.producer import Producer

logger = logging.getLogger(__name__)


class MainService:
    def __init__(self, llm: LlmService, kb: KnowledgeBaseService, dispatcher: DispatcherService, producer: Producer):
        self.llm = llm
        self.kb = kb
        self.dispatcher = dispatcher
        self.producer = producer
        self.executor = ThreadPoolExecutor(max_workers=2)
        logger.info("MainService initialized.")

    def handle_message(self, message: dict):
        logger.info(f"Received message for processing")
        try:
            text = message.get('text')
            if not text:
                raise ValueError("Message does not contain 'text' field")

            logger.info(f"Extracting problem from text: {text}")
            problem = self.llm.extract_problem_and_category(text=str(text))

            logger.info(f"Searching for solutions to problem: {problem}")
            future_solution = self.executor.submit(self.kb.find_solution, problem, top_k=1)
            solutions = future_solution.result(timeout=30)
            if len(solutions) == 1:
                solution = solutions[0]
            else:
                solution = Solution(title="No solution found", url="")

            logger.info(f"Routing problem to appropriate destination.")
            future_destination = self.executor.submit(self.dispatcher.route_problem, problem)
            destination = future_destination.result(timeout=30)

            result = {
                'input': text,
                'problem': problem.model_dump(),
                'solutions': solution.model_dump(),
                'destination': destination
            }
            logger.info(f"Sending final result: {result}")
            self.producer.send(result)
        except TimeoutError as e:
            logger.error("Timeout occurred while processing message.")
        except Exception as e:
            logger.exception(f"Unhandled exception during message handling: {e}")
