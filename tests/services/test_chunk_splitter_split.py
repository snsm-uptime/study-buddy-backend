import pytest
from app.services import ChunkSplitterService
from app.schemas.file_chunk import PageText
from pydantic import BaseModel


class MockFileChunk(BaseModel):
    text: str
    chunk_index: int
    page_numbers: list[int]
    section: None
    file_name: str


@pytest.fixture
def splitter():
    return ChunkSplitterService(
        model_name="cl100k_base",  # or your real encoding
        max_tokens=10,
        min_last_chunk=5,
        overlap=2,
    )


@pytest.mark.asyncio
async def test_splitter_tracks_page_numbers_correctly(splitter):
    pages = [PageText(text="Hello world. " * i, page_number=i) for i in range(20)]

    chunks = list(splitter.split(pages, file_name="test.txt"))

    assert len(chunks) >= 2
    for chunk in chunks:
        assert isinstance(chunk.page_numbers, list)
        assert len(chunk.page_numbers) > 0
        assert all(isinstance(p, int) for p in chunk.page_numbers)
        assert chunk.chunk_index >= 0
        assert chunk.file_name == "test.txt"

    # Ensure we captured both page 1 and 2
    seen_pages = set()
    for c in chunks:
        seen_pages.update(c.page_numbers)

    assert 1 in seen_pages and 2 in seen_pages
