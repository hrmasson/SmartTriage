import logging

import joblib
import pandas as pd

from orchestrator.dtos import Problem

logger = logging.getLogger(__name__)


class DispatcherService:
    def __init__(self, model_path: str, labels_path: str):
        try:
            self.model = joblib.load(model_path)
            self.label_encoder = joblib.load(labels_path)
            logger.info(f"Model and labels loaded successfully from: {model_path}, {labels_path}")
        except Exception as e:
            logger.exception(f"Failed to load model or labels: {e}")
            raise

    def route_problem(self, problem: Problem) -> str:
        try:
            if not problem.problem or not problem.category:
                raise ValueError("Problem or category is empty or None.")

            fulltext = f"{problem.problem} {problem.category}"
            logger.debug(f"Routing input: {fulltext}")

            X_input = pd.Series([fulltext])
            prediction = self.model.predict(X_input)

            label = self.label_encoder.inverse_transform(prediction)[0]
            logger.info(f"Routed to: {label}")
            return label

        except Exception as e:
            logger.exception(f"Failed to route problem: {e}")
            raise
