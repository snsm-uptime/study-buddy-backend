from pathlib import Path

import pytest
from returns.io import IOSuccess, IO
from returns.pipeline import is_successful

from app.services.parsers import PDFPlumberParser
from app.schemas.file_chunk import ChunkData

ASSETS_DIR = Path("tests") / "assets"


@pytest.mark.asyncio
async def test_pdf_parser_extracts_chunks_correctly():
    parser = PDFPlumberParser()
    file_path = ASSETS_DIR / "example_pdf.pdf"

    with file_path.open("rb") as file:
        result = await parser.parse(file)
    assert is_successful(
        result
    ), f"Expected Success, got Failure: {result.failure() if result.is_failure else ''}"

    chunks = result.unwrap()

    assert chunks.map(lambda x: isinstance(x, list))

    for i, chunk in enumerate(chunks):
        assert IO.do(c[i].chunk_index == i for c in chunks),
        f"Expected chunk_index={i}, got {chunk.chunk_index}"


@pytest.mark.asyncio
async def test_pdf_parser_uses_ocr_on_scanned_pdf():
    parser = PDFPlumberParser()
    file_path = ASSETS_DIR / "scanned_pdf.pdf"

    with file_path.open("rb") as file:
        result = await parser.parse(file)

    assert is_successful(
        result
    ), f"OCR fallback failed: {result.failure() if result.is_failure else ''}"

    chunks = result.unwrap()

    assert chunks.map(lambda x: isinstance(x, list))

    for chunk in chunks:
        assert isinstance(chunk.content, str)
        assert chunk.content.strip() != "", "Chunk content is empty after OCR"
