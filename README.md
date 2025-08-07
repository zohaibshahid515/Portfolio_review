# 🧾 Document Intelligence Pipeline with Azure & OpenAI

This project implements a robust, scalable, and intelligent document processing pipeline that extracts, classifies, and validates structured data from scanned documents (PDFs and images). It combines the power of **Azure AI Document Intelligence (Layout Model)** and **Azure OpenAI (GPT-4o & o4-mini)** to enable dynamic, rule-driven document understanding.

---

## 🚀 Tech Stack

- **Azure AI Document Intelligence** (Layout Model v4.0) – For OCR & layout-level parsing of scanned PDFs/PNGs.
- **Azure OpenAI (GPT-4o / o4-mini)** – For:
  - Intelligent section classification
  - Structured field extraction
  - Validation logic
- **Python** – Core orchestration
- **Streamlit** *(Optional)* – For local interface
- **Modular File Structure** – `openai_client.py`, `layout_model.py`, `storage.py`, `classification.py`, etc.

---

## 📁 Core Modules

### `openai_client.py`
Handles communication with Azure OpenAI. Key methods include:

- `get_best_title()` → Matches page to document title
- `get_structured_json_from_prompt()` → Extracts structured fields from raw OCR
- `classify_section()` → Classifies a page into one of 7 sections
- `validate_section()` → Validates whether a page meets section rules

### `pdf_processor.py`
Responsible for calling Azure Document Intelligence Layout Model and extracting page-wise content (lines, tables, handwriting, etc.).

### `page_classifier.py`
Defines matching rules and prompt engineering logic for 7 main document sections.

---

## 🧠 Supported Document Sections

| Section | Purpose |
|--------|---------|
| `Official_Training_Documentation` | Includes training summaries, education transcripts, certificates |
| `Family_Questionnaires` | Parent/guardian feedback |
| `Reflective_Dialogue_Worksheet` | Boxes A & B: Areas of strength and growth |
| `Reflective_Statements_of_Competence` | Functional Area reflections for goals I–VI |
| `Resource_Collection` | CDA resource collections (RC I–VI), safety training, lesson plans |
| `Reflective_Professional_Philosophy_Statement` | Candidate’s early childhood education philosophy |
| `Unmatched` | For pages not clearly matching any category (based on rules or OCR noise) |

---

## 🔁 Workflow Overview

```
flowchart TD
    A[Upload PDF or PNG] --> B[Azure Layout Model]
    B --> C[Extracted Page Content]
    C --> D[Title Matching (GPT-4o)]
    D --> E[Section Classification]
    E --> F[Structured JSON Extraction]
    F --> G[Validation Rules (Optional)]
    G --> H[Final JSON Output per Page]
