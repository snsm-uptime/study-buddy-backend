from pathlib import Path

import pytest
from returns.io import IOSuccess

from app.services.parsers import PDFPlumberParser
from app.schemas.file_chunk import ChunkData

ASSETS_DIR = Path("tests") / "assets"


@pytest.mark.asyncio
async def test_pdf_parser_extracts_chunks_correctly():
    parser = PDFPlumberParser()
    file_path = ASSETS_DIR / "example_pdf.pdf"

    with file_path.open("rb") as file:
        result = await parser.parse(file)

    assert isinstance(
        result, IOSuccess
    ), f"Expected Success, got Failure: {result.failure() if result.is_failure else ''}"

    chunks = result.unwrap()

    assert isinstance(chunks, list), "Result is not a list"
    assert all(
        isinstance(chunk, ChunkData) for chunk in chunks
    ), "Not all elements are ChunkData"
    assert len(chunks) > 0, "No chunks returned"

    for i, chunk in enumerate(chunks):
        assert (
            chunk.chunk_index == i
        ), f"Expected chunk_index={i}, got {chunk.chunk_index}"
        assert (
            chunk.page_number == i + 1
        ), f"Expected page_number={i+1}, got {chunk.page_number}"
        assert isinstance(chunk.content, str)
        assert chunk.content.strip() != ""


@pytest.mark.asyncio
async def test_pdf_parser_uses_ocr_on_scanned_pdf():
    parser = PDFPlumberParser()
    file_path = ASSETS_DIR / "scanned_pdf.pdf"

    with file_path.open("rb") as file:
        result = await parser.parse(file)

    assert isinstance(
        result, IOSuccess
    ), f"OCR fallback failed: {result.failure() if result.is_failure else ''}"
    chunks = result.unwrap()

    assert len(chunks) > 0, "No chunks returned from OCR fallback"

    for chunk in chunks:
        assert isinstance(chunk.content, str)
        assert chunk.content.strip() != "", "Chunk content is empty after OCR"
