from pathlib import Path

import pdfplumber
import pytesseract
from returns.future import future_safe

from app.errors import TextExtractionError
from app.protocols.parser import FileParser


class PDFPlumberParser(FileParser):
    """Functional parser for PDFs using pdfplumber with OCR fallback."""

    @future_safe
    async def extract_text(self, file_path: Path) -> str:
        try:
            text_segments = []

            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text and text.strip():
                        text_segments.append(text)
                    else:
                        image = page.to_image(resolution=300).original
                        ocr_text = pytesseract.image_to_string(image)
                        text_segments.append(ocr_text)

            return "\n".join(text_segments)
        except Exception as e:
            raise TextExtractionError(f"Failed to parse PDF: {str(e)}") from e
