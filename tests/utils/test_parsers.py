from pathlib import Path

from typing import List

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

    io_chunks = result.unwrap()

    assert io_chunks.map(lambda x: isinstance(x, list))

    def check_indexes(chunks: List[ChunkData]) -> bool:
        for index, chunk in enumerate(chunks):
            assert (
                chunk.chunk_index == index
            ), f"Expected chunk_index={index}, got {chunk.chunk_index}"

    IO.do(check_indexes(c) for c in io_chunks)


@pytest.mark.asyncio
async def test_pdf_parser_uses_ocr_on_scanned_pdf():
    parser = PDFPlumberParser()
    file_path = ASSETS_DIR / "short_scanned_pdf.pdf"

    with file_path.open("rb") as file:
        result = await parser.parse(file)

    assert is_successful(
        result
    ), f"OCR fallback failed: {result.failure() if result.is_failure else ''}"

    io_chunks = result.unwrap()

    assert io_chunks.map(lambda x: isinstance(x, list))

    def check_indexes(chunks: List[ChunkData]) -> bool:
        for index, chunk in enumerate(chunks):
            assert (
                chunk.chunk_index == index
            ), f"Expected chunk_index={index}, got {chunk.chunk_index}"

    IO.do(check_indexes(c) for c in io_chunks)
