# app/config/validation_rules.py

# app/services/validation_rules.py

# VALIDATION_PROMPT = """
# You are a CDA Portfolio Section Validator.

# Task:
# - Evaluate whether the given page content meets the requirements for the section: {section}.
# - Follow strict rules for the section from the CDA portfolio requirements.
# - Return "YES" if all key criteria are met, otherwise "NO" with a reason.

# Rules:
# - Do not be lenient. A small missing requirement should result in "NO".
# - Base your decision only on the provided page content.

# Output must follow the SectionValidationResult schema.
# """


VALIDATION_RULES = {
    "Official_Training_Documentation": [
        "**Total documented training time must be at least 120 clock hours across all pages in this section.**",
        "**At least one valid transcript, certificate, or letter must be present depicting course completion.**",
        "**At least one document in this section must clearly display ALL of the following:** training agency name and address, course name, Specified Subject Area (if applicable), candidate name, total hours/credits, dates of training, and signature of an authorized person.",
        "**'Summary of My CDA Education' sheet:** All 8 CDA Subject Areas must have initials provided (content of initials is not validated). Candidate’s signature and date must also be present somewhere in this section.",
        "**'My CDA Professional Portfolio' page:** Third column (Selection Marks) must have **at least 18 marks selected**. More than 18 is acceptable, fewer than 18 fails the rule.",
        "**'Summary of My CDA Education' page:** In the CDA Subject Areas table, the second column (which may be titled 'Initials' or similar) must be filled for all 8 rows. Values are not validated for correctness, only for presence."
    ],

    "Family_Questionnaires": [
        "**Section must include a summary of Family Questionnaire responses.**",
        "**The total number of forms distributed and number received must be mentioned anywhere in this section.**",
        "**At least one page must identify areas of strength as reported by families.**",
        "**At least one page must identify areas for professional growth based on family feedback.**",
        "**Areas for growth should align with the Reflective Dialogue Worksheet (cross-checking is required).**"
    ],

    "Reflective_Dialogue_Worksheet": [
        "**At least one page must clearly be labeled as Reflective Dialogue Worksheet.**",
        "**The section must contain Box A (Strengths) content somewhere in the section.**",
        "**The section must contain Box B (Areas for Growth) content somewhere in the section.**",
        "**Growth areas listed in Box B must align with Family Questionnaire results (alignment check is based on presence of related terms).**"
    ],

    "Reflective_Statements_of_Competence": [
        "**The section must include exactly six competency statements — one for each CDA Competency Goal.**",
        "**Each statement must have a length between 200 and 500 words (approximate length is acceptable).**",
        "**Each statement must explain how candidate practices meet the CDA Standards.**",
        "**If the assessment is bilingual: at least three statements in English and at least three in the second language.**",
        "**Each statement must reference the Functional Areas related to its CDA Goal.**"
    ],

    "Resource_Collection": [
        "**Section must include references to all required Resource Collection items (RC I-1 through RC VI-3).**",
        "**At least one page must contain evidence of a valid First Aid/CPR certificate.**",
        "**At least one weekly lesson plan must be present in this section.**",
        "**At least one page must include legal requirements (e.g., Child Abuse and Neglect summary).**",
        "**At least one page must include resources for families or references to professional associations.**"
    ],

    "Reflective_Professional_Philosophy_Statement": [
        "**Section must include a document titled 'Professional Philosophy Statement'.**",
        "**The statement must describe the candidate’s beliefs about early childhood education.**",
        "**The statement must answer the question: 'How do young children learn?'.**",
        "**The statement must answer the question: 'What is the candidate’s role in supporting learning?'.**",
        "**The statement must be no longer than 500 words or 2 pages in length.**"
    ]
}
