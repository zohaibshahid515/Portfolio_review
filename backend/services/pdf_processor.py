# app/services/pdf_processor.py

import base64
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from pathlib import Path
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from config.setting import DOCUMENT_INTELLIGENCE_ENDPOINT, DOCUMENT_INTELLIGENCE_KEY
from services.logger import get_logger

logger = get_logger(__name__)

class PDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.client = DocumentIntelligenceClient(
            endpoint=DOCUMENT_INTELLIGENCE_ENDPOINT,
            credential=AzureKeyCredential(DOCUMENT_INTELLIGENCE_KEY)
        )

    def split_pdf(self) -> list[BytesIO]:
        """Split PDF into single-page streams."""
        reader = PdfReader(str(self.pdf_path))
        pages = []
        for page in reader.pages:
            writer = PdfWriter()
            writer.add_page(page)
            stream = BytesIO()
            writer.write(stream)
            stream.seek(0)
            pages.append(stream)
        logger.info(f"Split PDF into {len(pages)} page(s).")
        return pages

    def analyze_single_page(self, page_stream: BytesIO) -> str:
        """Analyze one page via Layout endpoint."""
        logger.info("Analyzing one page of PDF")
        base64_data = base64.b64encode(page_stream.read()).decode("utf-8")
        poller = self.client.begin_analyze_document(
            model_id="prebuilt-layout",
            analyze_request={"base64Source": base64_data}
        )
        result = poller.result()
        return result.content  # content is just that page's text
    def analyze_with_layout_model(self) -> list[dict]:
        """
        Extracts content from each page of the PDF using Layout Model.

        Returns:
            list[dict]: Each dict contains 'page_number' and 'text'.
        """
        contents = []
        for idx, page_stream in enumerate(self.split_pdf()):
            text = self.analyze_single_page(page_stream)
            logger.info(f"Extracted {len(text)} chars from page {idx + 1}")
            contents.append({
                "page_number": idx + 1,
                "text": text
            })
            
            if idx == 2:
                pass
                # print("content for page 3 is : ", text)

                
        return contents
