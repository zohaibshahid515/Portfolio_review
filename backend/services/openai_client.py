# backend/services/openai_client.py
from openai import AzureOpenAI
from config.setting import OPENAI_API_KEY
import json

class OpenAIClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=OPENAI_API_KEY,
            api_version="2025-01-01-preview",
            azure_endpoint="https://zohai-mdho0prb-eastus2.cognitiveservices.azure.com/"
        )

        self.classification_deployment = "o4-mini"
        self.json_deployment = "gpt-4o"

    def get_best_title(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.classification_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content.strip()

    def get_structured_json_from_prompt(self, system_prompt: str, user_prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.json_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"}
        )
        raw = response.choices[0].message.content
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse structured output:\n{raw}")

    def classify_section(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.classification_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content.strip()

    def validate_section(self, system_prompt: str, user_prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.json_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"}
        )
        raw = response.choices[0].message.content
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse validation structured output:\n{raw}")
