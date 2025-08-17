from fastapi import FastAPI, UploadFile, File
import tempfile
import os
from pipeline.phase_one import PhaseOnePipeline

app = FastAPI()

@app.post("/run-pipeline")
async def run_pipeline(file: UploadFile = File(...)):
    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(await file.read())
        pdf_path = tmp_file.name

    # Run pipeline
    pipeline = PhaseOnePipeline(
        pdf_path=pdf_path,
        titles_config_path="data/titles_config.json"
    )
    retrieved_sections = pipeline.run()

    # Add Divider/Cover Sheets condition
    unique_sections = retrieved_sections.get("unique_sections", []).copy()
    if retrieved_sections.get("section_1", 0) >= 3:
        if "Divider/Cover Sheets" not in unique_sections:
            unique_sections.append("Divider/Cover Sheets")

    # Compute status
    ALL_SECTIONS = [
        'Family_Questionnaires',
        'Official_Training_Documentation',
        'Reflective_Dialogue_Worksheet',
        'Reflective_Professional_Philosophy_Statement',
        'Reflective_Statements_of_Competence',
        'Resource_Collection',
        'Divider/Cover Sheets',
    ]
    completed = unique_sections
    incomplete = [sec for sec in ALL_SECTIONS if sec not in completed]

    return {
        "completed": completed,
        "incomplete": incomplete,
        "summary": f"Completed: {len(completed)} / {len(ALL_SECTIONS)}"
    }


@app.get("/ping")
def ping():
    return {"status": "ok"}