import os
import json
from services.section_validator import SectionValidator

class SectionLevelValidator:
    def __init__(self, base_output="outputs"):
        self.base_output = base_output
        self.validator = SectionValidator()

    def _merge_section_pages(self, section_path: str) -> dict:
        """
        Loads all JSON files in a section folder and merges into one dict.
        The merged dict will have a 'pages' list containing all page data.
        """
        merged_data = {"pages": []}

        for file_name in sorted(os.listdir(section_path)):  # sort to keep order
            if file_name.endswith(".json"):
                file_path = os.path.join(section_path, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        page_data = json.load(f)
                        merged_data["pages"].append(page_data)
                    except json.JSONDecodeError:
                        merged_data["pages"].append({"error": f"Invalid JSON in {file_name}"})
        return merged_data

    def validate_all_sections(self, section_folders: list[str]) -> dict:
        """
        Validates each section as a whole by merging all pages into one object.
        Returns dictionary with validation results.
        """
        validation_summary = {}
        # print("section folders : ", section_folders)
        for section in section_folders:
            section_path = os.path.join(self.base_output, section)

            if os.path.exists(section_path):
                merged_data = self._merge_section_pages(section_path)
                # print("/n#############################33merged json files against each section : ")
                # print("/n ", section)
                # print(merged_data)
                # print("/n#################################3")
                if merged_data["pages"]:
                    # Pass merged JSON to LLM validator
                    result = self.validator.validate(section, merged_data)
                    validation_summary[section] = result
                else:
                    validation_summary[section] = {
                        "valid": False,
                        "reasons": ["No pages found in this section"]
                    }
            else:
                validation_summary[section] = {
                    "valid": False,
                    "reasons": ["Section folder missing"]
                }

        return validation_summary
