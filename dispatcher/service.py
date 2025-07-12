import joblib
import pandas as pd
from orchestrator.dtos import Problem

class DispatcherService:
    def __init__(self, model_path: str, labels_path: str):
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(labels_path)

    def route_problem(self, problem: Problem) ->str:
        fulltext = problem.problem + ' ' + problem.category

        X_input = pd.Series([fulltext])
        prediction = self.model.predict(X_input)

        return self.label_encoder.inverse_transform(prediction)[0]