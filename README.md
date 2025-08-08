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
| `Divider/Cover Sheets` | 3 key ones implied |
| `Official_Training_Documentation` | Includes training summaries, education transcripts, certificates |
| `Family_Questionnaires` | Parent/guardian feedback |
| `Reflective_Dialogue_Worksheet` | Boxes A & B: Areas of strength and growth |
| `Reflective_Statements_of_Competence` | Functional Area reflections for goals I–VI |
| `Resource_Collection` | CDA resource collections (RC I–VI), safety training, lesson plans |
| `Reflective_Professional_Philosophy_Statement` | Candidate’s early childhood education philosophy |


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

## 1️⃣ Create & Activate Virtual Environment (Python 3.13.5)

```bash
# Create virtual environment
python3.13 -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate
```

## 2️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 3️⃣ Run the Streamlit App

```bash
streamlit run run_phase_1.py
```

## 4️⃣ Environment Variables
Store sensitive keys in a .env file (never commit this to Git):

```bash
AZURE_API_KEY=your-azure-ai-key
AZURE_ENDPOINT=your-azure-endpoint
OPENAI_API_KEY=your-openai-key
```

## 5️⃣ Stop the App
Press CTRL+C in the terminal to stop the Streamlit server.