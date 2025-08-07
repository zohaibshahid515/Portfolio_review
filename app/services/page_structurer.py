# app/services/page_structurer.py

import json
from config.setting import TITLES_CONFIG_PATH
from app.services.openai_client import OpenAIClient


class PageStructurer:
    """
    Converts unstructured page text into structured JSON using title-specific prompts defined
    in a configuration file. Uses OpenAI to extract structured data.
    """

    def __init__(self):
        """
        Loads title-to-prompt mappings and initializes the OpenAI client.
        """
        with open("data/titles_config.json", "r", encoding="utf-8") as f:
            self.prompt_config = json.load(f)
        self.openai_client = OpenAIClient()

    def structure_page(self, title: str, page_content: str) -> dict:
        """
        Structures unstructured page content into a JSON object by:
        - Fetching the prompt associated with the matched title
        - Injecting the extracted page content into the prompt
        - Calling OpenAI to parse the content into structured JSON

        Args:
            title (str): The matched title for this page (from title matcher).
            page_content (str): The full text content of the page.

        Returns:
            dict: A structured representation of the page's data.

        Raises:
            ValueError: If title is not found in the prompt config or output is not valid JSON.
        """
        if title not in self.prompt_config:
            raise ValueError(f"No prompt found for title '{title}'")

        # Inject page content into prompt template
        raw_prompt = self.prompt_config[title]["prompt"]
        filled_prompt = raw_prompt.replace("{page}", page_content)

        # Define the system role
        system_prompt = (
            f"You are an AI assistant that extracts structured information from early childhood education pages.\n\n"
            f"Given the content of a page, return a JSON object with the extracted fields required for the title: '{title}'.\n"
            f"If information is missing, use null.\n"
            f"Return only valid JSON — no extra text, explanations, or formatting."
        )

        # Send to OpenAI
        structured_output = self.openai_client.get_structured_json_from_prompt(
            system_prompt=system_prompt,
            user_prompt=filled_prompt
        )

        try:
            return structured_output
        except json.JSONDecodeError:
            raise ValueError(f"Model returned non-JSON output:\n{structured_output}")
