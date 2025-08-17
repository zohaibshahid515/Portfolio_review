# run_phase_1.py (Streamlit Dashboard)

import streamlit as st
import tempfile
import os
from app.pipeline.phase_one import PhaseOnePipeline
from app.services.section_level_validator import SectionLevelValidator

# Define all required sections
ALL_SECTIONS = [
    'Family_Questionnaires',
    'Official_Training_Documentation',
    'Reflective_Dialogue_Worksheet',
    'Reflective_Professional_Philosophy_Statement',
    'Reflective_Statements_of_Competence',
    'Resource_Collection',
    'Divider/Cover Sheets',
]

# Streamlit Page Config
st.set_page_config(page_title="Phase 1 PDF Processor", layout="wide")
st.title("📄 Phase 1 PDF Processing Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    # Temporary save path for PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    # NEXT button triggers pipeline
    if st.button("NEXT ▶️"):
        with st.spinner("Processing PDF... Please wait"):
            # Always run fresh pipeline
            pipeline = PhaseOnePipeline(
                pdf_path=pdf_path,
                titles_config_path="data/titles_config.json"
            )
            retreived_sections = pipeline.run()

            # # Debug: Show raw pipeline output
            # st.subheader("🔍 Debug: Raw Unique Sections from Pipeline")
            # st.write(retreived_sections.get("unique_sections", []))

            # Make fresh copy of unique sections each run
            unique_sections = retreived_sections.get("unique_sections", []).copy()

            # Add Divider/Cover Sheets condition
            if retreived_sections.get("section_1", 0) >= 3:
                if "Divider/Cover Sheets" not in unique_sections:
                    unique_sections.append("Divider/Cover Sheets")

        # Section Lists
        completed = unique_sections
        incomplete = [sec for sec in ALL_SECTIONS if sec not in completed]

        # Display Results
        st.subheader("📋 Section Status")
        st.markdown(f"**Completed: {len(completed)} / {len(ALL_SECTIONS)}**")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Completed Sections")
            if completed:
                for sec in completed:
                    st.success(sec)
            else:
                st.info("No sections completed yet.")

        with col2:
            st.markdown("### ⚠️ Incomplete Sections")
            if incomplete:
                for sec in incomplete:
                    st.warning(sec)
            else:
                st.success("All sections are complete! 🎉")

        # # Optional: Show Output JSON Files
        # outputs_path = os.path.join("outputs")
        # if os.path.exists(outputs_path):
        #     st.subheader("📂 Output Files")
        #     for root, dirs, files in os.walk(outputs_path):
        #         for file in files:
        #             st.text(os.path.join(root, file))
