import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()  # adjust path if needed
BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(page_title="Phase 1 PDF Processor", layout="wide")
st.title("📄 Phase 1 PDF Processing Dashboard")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("NEXT ▶️"):
        with st.spinner("Processing PDF... Please wait"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            try:
                response = requests.post(BACKEND_URL, files=files)
                response.raise_for_status()
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
            else:
                data = response.json()
                completed = data.get("completed", [])
                incomplete = data.get("incomplete", [])
                summary = data.get("summary", "")

                # Show summary
                st.subheader("📋 Section Status")
                st.markdown(summary)

                # Display completed and incomplete sections
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
                        st.success("All sections complete! 🎉")
