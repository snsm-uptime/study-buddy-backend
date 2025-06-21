import asyncio
import io
from typing import BinaryIO

import pdfplumber
import pytesseract
from returns.future import future_safe, FutureResult

from app.protocols.parser import FileParserProtocol
from app.schemas.file_chunk import ChunkData
from app.errors import TextExtractionError


class PDFPlumberParser(FileParserProtocol):
    """Parses PDF files into chunks using pdfplumber with OCR fallback per page."""

    @future_safe
    def parse(self, file: BinaryIO) -> FutureResult[list[ChunkData], str]:
        return asyncio.to_thread(self._parse_sync, file)

    def _parse_sync(self, file: BinaryIO) -> list[ChunkData]:
        try:
            file_bytes = file.read()
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                chunks = []
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if not text or not text.strip():
                        image = page.to_image(resolution=300).original
                        text = pytesseract.image_to_string(image)

                    chunks.append(
                        ChunkData(
                            content=text,
                            chunk_index=i,
                            page_number=i + 1,
                            section=None,  # placeholder for future heading inference
                        )
                    )
                return chunks
        except Exception as e:
            raise TextExtractionError(f"Failed to parse PDF: {e}") from e
