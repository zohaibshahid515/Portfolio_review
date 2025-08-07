import logging
from app.services.openai_client import OpenAIClient  # ✅ Removed SectionValidationResult
from config.validation_rules import VALIDATION_RULES

logger = logging.getLogger(__name__)


class SectionValidator:
    def __init__(self):
        self.openai = OpenAIClient()

    def validate(self, section: str, structured_data: dict) -> dict:
        # print("in section validator.py and section returned is :  ", section)
        section_rule = VALIDATION_RULES[section]
        # print("/n section rules are : ",section_rule)
        system_prompt = f"""
        **Overall approach:**
        You are validating the ENTIRE section as a *whole*, based on structured JSON data
        that contains ALL pages merged for this section. 
        Do NOT validate page-by-page in isolation. 
        If a required element (e.g., signature, date, ID, selection marks) appears 
        in ANY page of the section, it satisfies the rule for the entire section.

        **'structured_data' format : **
        - The `structured_data` contains JSON objects for all pages classified under this section.
        - Each page starts with a key "title".
        - Information relevant to validation can appear on ANY page within the section.
        - The same information may be repeated across pages (e.g., candidate signature on multiple pages).

        **Validation approach:**
        - Treat the entire section as a whole. Do NOT require the same item to appear on every page.
        - If a requirement is satisfied on any single page, it is considered fulfilled for the section.
        - Overlapping or duplicate information across pages is acceptable and should not be penalized.

        **Important evaluation rule:**
        - If a required item (signature, date, ID, selection marks, etc.) appears in ANY page of the section, it should be considered PRESENT for the whole section.
        - Do NOT fail the section for missing items on individual pages if they are present elsewhere in the section.


        **Evaluation principles:**
        - Evaluate ONLY against the rules for this section.
        - A rule is UNSATISFIED only if:
        - It is missing across ALL pages in the section.
        - The content clearly contradicts the rule.
        - If a rule specifies a minimum (e.g., "at least 18 marks"), having more than that is acceptable unless it invalidates the format.
        - Do NOT penalize extra valid details or better formatting.
        - Ignore satisfied rules completely in the "reasons" list.



        **Output format:**
        Return strictly in JSON:
        {{
        "status": "YES" or "NO",
        "reasons": ["List of concise reasons for failure if status is NO"]
        }}
        """

        user_prompt = f"Section: {section}\nStructured Data: {structured_data}\n and rules for the section are {section_rule}"
        return self.openai.validate_section(system_prompt, user_prompt)
