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
            "Your task is to determine the correct title of a single page strictly from the provided list of titles.\n\n"
            "INSTRUCTIONS:\n"
            "1. The decision should be based primarily on the first few lines, headings, or any bold/capitalized phrases at the top of the page.\n"
            f"2. The ONLY allowed choices are exactly these titles:\n{list_of_titles}\n\n"
            "3. You must pick one title from this list—no new titles, no modifications, no guesses outside the list.\n"
            "4. If no explicit match is found, choose the closest match from the list based on exact wording or clear synonyms.\n"
            "5. If multiple titles seem possible, choose the one that best matches the majority of the page content.\n"
            "6. Always return ONLY the chosen title string, without explanation or reasoning.\n"
        )



        if not isinstance(content, str):
            raise TypeError(f"Expected string content, got {type(content)}: {content}")

        user_prompt = f"Page Content:\n\n{content}"
        selected_title = self.openai_client.get_best_title(system_prompt, user_prompt)
        # print("####################################")
        # print("selected title : ", selected_title)
        return selected_title
