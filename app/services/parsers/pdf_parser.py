import asyncio
import io
from typing import BinaryIO, List

import pdfplumber
import pytesseract
from returns.future import future_safe

from app.errors import TextExtractionError
from app.protocols.parser import FileParserProtocol
from app.schemas.file_chunk import PageText


class PDFPlumberParser(FileParserProtocol):
    """Parses PDF files into chunks using pdfplumber with OCR fallback per page."""

    async def parse(self, file: BinaryIO) -> List[PageText]:
        return await asyncio.to_thread(self._parse_sync, file)

    def _parse_sync(self, file: BinaryIO) -> List[PageText]:
        try:
            file_bytes = file.read()
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                pages = []
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if not text or not text.strip():
                        image = page.to_image(resolution=300).original
                        text = pytesseract.image_to_string(image)

                    pages.append(PageText(text=text, page_number=i))
                return pages
        except Exception as e:
            raise TextExtractionError(f"Failed to parse PDF: {e}") from e
