from concurrent.futures import ThreadPoolExecutor
from llm.service import LlmService
from knowledge_base.service import KnowledgeBaseService
from dispatcher.service import DispatcherService
from orchestrator.dtos import Solution
from rabbit.producer import Producer

class MainService:
    def __init__(self, llm: LlmService, kb: KnowledgeBaseService, dispatcher: DispatcherService, producer: Producer):
        self.llm = llm
        self.kb = kb
        self.dispatcher = dispatcher
        self.producer = producer
        self.executor = ThreadPoolExecutor(max_workers=2)

    def handle_message(self, message: dict):
        text = message['text']
        problem = self.llm.extract_problem_and_category(text=str(text))

        solutions = self.executor.submit(self.kb.find_solution, problem, top_k=1).result()
        if len(solutions) == 1:
            solution = solutions[0]
        else:
            solution = Solution(title="No solution found", url="")

        destination = self.executor.submit(self.dispatcher.route_problem, problem).result()

        result = {
            'input': text,
            'problem': problem.model_dump(),
            'solutions': solution.model_dump(),
            'destination': destination
        }
        self.producer.send(result)