import json
import logging
import re

import requests
from requests import Response

from llm.base import LLMClient
from orchestrator.dtos import Problem

logger = logging.getLogger(__name__)


class LocalAIClient(LLMClient):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model
        logger.info(f"Initialized LocalAIClient with base_url={self.base_url}, model={self.model}")

    def __extract_json(self, response: Response) -> Problem:
        try:
            logger.debug("Extracting JSON from LLM response")
            content = response.json()["choices"][0]["message"]["content"]
            match = re.search(r"\{.*}", content, re.DOTALL)
            if not match:
                logger.warning("No JSON object found in response content.")
                raise ValueError("No JSON object found in response")
            json_data = json.loads(match.group())
            logger.info("Successfully parsed JSON from LLM output.")
            return Problem(**json_data)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}\nRaw response: {response.text}")
            raise ValueError(f"Invalid JSON response: {e}\nRaw response: {response.text}")
        except Exception as e:
            logger.exception(f"Unexpected error during JSON extraction: {e}")
            raise

    def extract_problem_and_category(self, text: str) -> Problem:
        logger.info(f"Sending prompt to LLM for input: {text}")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an API that extracts structured information from text. "
                    "You must return only a JSON object with:\n"
                    "- 'problem': a short summary (5–10 words) rephrased in your own words\n"
                    "- 'category': one-word category like 'hardware', 'network', etc.\n"
                    "No explanations, no formatting, no markdown."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Extract the problem and the category from the following message:\n\n"
                    f"\"{text}\"\n\n"
                    "Summarize the problem in your own words (5–10 words max).\n"
                    "Return JSON in the form:\n"
                    "{\n  \"problem\": \"...\",\n  \"category\": \"...\"\n}"
                )
            }
        ]
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.2,
                    "max_tokens": 300
                },
                timeout=90
            )
            response.raise_for_status()
            if response.status_code != 200:
                logger.error(f"LLM returned error {response.status_code}: {response.text}")
                raise ValueError(f"Error {response.status_code}: {response.text}")
            logger.debug("Received valid response from LLM.")
            return self.__extract_json(response)
        except requests.RequestException as e:
            logger.exception(f"Request to LLM failed: {e}")
            raise
