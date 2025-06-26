from pathlib import Path
from typing import List

import pytest
from returns.io import IO, IOSuccess
from returns.pipeline import is_successful

from app.schemas.file_chunk import FileChunkBase
from app.services.parsers import PDFPlumberParser

ASSETS_DIR = Path("tests") / "assets"


@pytest.mark.asyncio
async def test_pdf_parser_extracts_chunks_correctly():
    parser = PDFPlumberParser()
    file_path = ASSETS_DIR / "example_pdf.pdf"

    with file_path.open("rb") as file:
        result = await parser.parse(file)

    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) > 0, "Expected non-empty list of chunks"


@pytest.mark.asyncio
async def test_pdf_parser_uses_ocr_on_scanned_pdf():
    parser = PDFPlumberParser()
    file_path = ASSETS_DIR / "short_scanned_pdf.pdf"

    with file_path.open("rb") as file:
        result = await parser.parse(file)

    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) > 0, "Expected non-empty list of chunks"
