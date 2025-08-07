#app/services/title_matcher.py
import json
from pathlib import Path
from app.services.openai_client import OpenAIClient

class TitleMatcher:
    def __init__(self, titles_config_path: str):
        self.config_path = Path(titles_config_path)
        with self.config_path.open("r", encoding="utf-8") as f:
            self.titles_config = json.load(f)
        self.openai_client = OpenAIClient()

    def match_title(self, content: str) -> str:
        list_of_titles = list(self.titles_config.keys())
        # print("list if titles : ", list_of_titles)
        system_prompt = (
            "You are an expert in CDA Portfolio document classification. "
            "Your task is to determine the correct title of a single page by comparing its content "
            "to a fixed list of allowed titles.\n\n"
            "INSTRUCTIONS:\n"
            "1. The decision should be based primarily on the first few lines, headings, or any bold/capitalized phrases at the top of the page.\n"
            "2. Choose ONLY from the provided titles:\n"
            f"{list_of_titles}\n\n"
            "3. If there is no clear or strong match, return EXACTLY 'unknown_title'.\n"
            "4. Do NOT create or guess new titles.\n"
            "5. Do NOT choose a title unless the match is explicit (exact wording, close synonyms, or obvious section heading).\n"
            "6. If multiple titles seem possible, pick the one that matches the majority of the page content.\n"
            "7. Always return ONLY the title string (no explanation, no reasoning).\n"
            "8. Your output must exactly match one of the provided titles or 'unknown_title'."
        )


        if not isinstance(content, str):
            raise TypeError(f"Expected string content, got {type(content)}: {content}")

        user_prompt = f"Page Content:\n\n{content}"
        selected_title = self.openai_client.get_best_title(system_prompt, user_prompt)
        # print("####################################")
        # print("selected title : ", selected_title)
        return selected_title
