import json

class KnowledgeBaseLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file {self.file_path} is not a valid JSON file.")
            return None