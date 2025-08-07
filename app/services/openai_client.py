# app/services/openai_client.py
from openai import AzureOpenAI
import json

from config.setting import OPENAI_API_KEY,OPENAI_ENDPOINT,AZURE_OPENAI_API_VERSION


class OpenAIClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=OPENAI_ENDPOINT
        )

        # Make sure these names exactly match Azure deployment names
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
        open_ai_response = response.choices[0].message.content.strip()
        # print("Title returned is:", open_ai_response)
        return open_ai_response

    def get_structured_json_from_prompt(self, system_prompt: str, user_prompt: str) -> dict:
        """Get JSON output safely from Azure OpenAI."""
        response = self.client.chat.completions.create(
            model=self.json_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"}  # ✅ Azure-compatible structured output
        )

        raw = response.choices[0].message.content
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse structured output:\n{raw}")

    def classify_section(self, system_prompt: str, user_prompt: str) -> str:
        """Classify a page into a section."""
        response = self.client.chat.completions.create(
            model=self.classification_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content.strip()

    def validate_section(self, system_prompt: str, user_prompt: str) -> dict:
        """Validate section compliance using structured JSON output."""
        response = self.client.chat.completions.create(
            model=self.json_deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"}  # ✅ Ensures JSON
        )

        raw = response.choices[0].message.content
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse validation structured output:\n{raw}")
