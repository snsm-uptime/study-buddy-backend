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
    assert is_successful(
        result
    ), f"Expected Success, got Failure: {result.failure() if result.is_failure else ''}"

    io_page_texts = result.unwrap()

    assert io_page_texts.map(lambda x: isinstance(x, list))

    def page_numbers(pages: List[FileChunkBase]) -> bool:
        for index, page in enumerate(pages):
            assert (
                page.page_number == index
            ), f"Expected page_number={index}, got {page.page_number}"

    IO.do(page_numbers(c) for c in io_page_texts)


@pytest.mark.asyncio
async def test_pdf_parser_uses_ocr_on_scanned_pdf():
    parser = PDFPlumberParser()
    file_path = ASSETS_DIR / "short_scanned_pdf.pdf"

    with file_path.open("rb") as file:
        result = await parser.parse(file)

    assert is_successful(
        result
    ), f"OCR fallback failed: {result.failure() if result.is_failure else ''}"

    io_page_texts = result.unwrap()

    assert io_page_texts.map(lambda x: isinstance(x, list))

    def page_numbers(pages: List[FileChunkBase]) -> bool:
        for index, page in enumerate(pages):
            assert (
                page.page_number == index
            ), f"Expected page_number={index}, got {page.page_number}"

    IO.do(page_numbers(c) for c in io_page_texts)
