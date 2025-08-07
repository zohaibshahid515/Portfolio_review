# app/pipeline/phase_one.py

import os
import json
import re
import shutil
from app.services.pdf_processor import PDFProcessor
from app.services.page_structurer import PageStructurer
from app.services.title_matcher import TitleMatcher
from app.services.page_classifier import PageClassifier
from app.services.section_validator import SectionValidator
import time


class PhaseOnePipeline:
    """
    Full pipeline:
    - Reads PDF
    - Analyzes each page
    - Assigns titles
    - Classifies section
    - Structures page content
    - Validates section compliance
    - Saves results
    """

    SECTION_FOLDERS = [
        "Official_Training_Documentation",
        "Family_Questionnaires",
        "Reflective_Dialogue_Worksheet",
        "Reflective_Statements_of_Competence",
        "Resource_Collection",
        "Reflective_Professional_Philosophy_Statement",
        "Unmatched"
    ]

    def __init__(self, pdf_path: str, titles_config_path: str):
        self.pdf_path = pdf_path
        self.title_matcher = TitleMatcher(titles_config_path)
        self.pdf_processor = PDFProcessor(pdf_path)
        self.structurer = PageStructurer()
        self.classifier = PageClassifier()
        self.validator = SectionValidator()

        # Store validation summary grouped by section
        self.validation_summary = {section: [] for section in self.SECTION_FOLDERS}

    def _prepare_output_folders(self):
        """Create and clean static section folders."""
        base_output = "outputs"
        os.makedirs(base_output, exist_ok=True)

        for section in self.SECTION_FOLDERS:
            folder_path = os.path.join(base_output, section)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)  # Clear folder
            os.makedirs(folder_path, exist_ok=True)  # Recreate empty folder

    def _normalize_section(self, section_name: str) -> str:
        """Map classifier output to valid folder key."""
        normalized = section_name.strip().replace(" ", "_")
        return normalized if normalized in self.SECTION_FOLDERS else "Unmatched"
    

    def run(self) -> dict:
        """Runs Phase One pipeline and returns results + validation summary."""
        self._prepare_output_folders()
        start_time = time.time()
        page_contents = self.pdf_processor.analyze_with_layout_model()
        end_time = time.time()

        print(f"[LLM Call - layout model] Time taken: {end_time - start_time:.2f} seconds")
        results = []

        section_1 = 0

        unique_sections = set()   # to quickly check duplicates
        section_list = []         # to preserve order

        for page in page_contents:
            page_num = page["page_number"]
            content = page["text"]

            # Step 1: Title detection
            start_time = time.time()
            title = self.title_matcher.match_title(content)
            end_time = time.time()
            print(f"[LLM Call - Title Matcher] Time taken: {end_time - start_time:.2f} seconds")


            if title == "My CDA professional portfolio" or "Summary of My CDA® Education" or "Family Questionnaires summary sheet":
                section_1 +=1


            # Step 2: Structured JSON
            start_time = time.time()
            structured = self.structurer.structure_page(title, content)
            end_time = time.time()
            print(f"[LLM Call - structuring into json] Time taken: {end_time - start_time:.2f} seconds")

            # Step 3: Section classification
            start_time = time.time()
            section = self.classifier.classify(title, structured)
            end_time - time.time()
            print(f"[LLM Call classification time] Time taken: {end_time - start_time:.2f} seconds")
            section_key = self._normalize_section(section)

            # Maintain unique section names
            if section_key not in unique_sections:
                unique_sections.add(section_key)
                section_list.append(section_key)

            # Step 4: Save JSON to correct folder
            save_dir = os.path.join("outputs", section_key)
            output_path = os.path.join(save_dir, f"page_{page_num}.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(structured, f, indent=2)

        return {
            "results": results,
            "unique_sections": section_list,
            "section_1":section_1
        }


            # Step 5: Validation
            # validation_result = self.validator.validate(section_key, structured)

            # # Add to validation summary
            # self.validation_summary[section_key].append({
            #     "page_num": page_num,
            #     "title": title,
            #     "valid": validation_result.get("valid", False),
            #     "missing_rules": validation_result.get("reasons", [])
            # })

            # # Add page result
            # results.append({
            #     "page_num": page_num,
            #     "title": title,
            #     "section": section_key,
            #     "structured_data": structured,
            #     "validation": {
            #         "valid": validation_result.get("valid", False),
            #         "missing_rules": validation_result.get("reasons", [])
            #     }
            # })

        # Return both page-wise results and section summary
        # return {
        #     "pages": results,
        #     "summary": self.validation_summary
        # }
