from pathlib import Path

import pytest
from returns.io import IOFailure, IOSuccess

from app.errors import TextExtractionError
from app.utils.parsers.pdf_parser import PDFPlumberParser

ASSETS_DIR = Path("tests") / "assets"


@pytest.mark.asyncio
async def test_pdf_parser_success():
    parse = PDFPlumberParser().extract_text
    test_pdf_path = ASSETS_DIR / "example_pdf.pdf"

    result = await parse(str(test_pdf_path))

    match result:
        case IOSuccess(res):
            text = res.unwrap()
            val = text.split("\n")[1]
            assert isinstance(text, str)
            assert val == "Sebastian Soto"
        case _:
            pytest.fail("Expected IOSuccess with text, but got failure.")
