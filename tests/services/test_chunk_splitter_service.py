import pytest

from app.services.chunk_splitter_service import ChunkSplitterService
from app.schemas.file_chunk import PageText


@pytest.mark.asyncio
async def test_chunk_splitter_merges_small_final_chunk():
    # Final segment is smaller than min_last_chunk → gets merged
    pages = [
        PageText(page_number=0, text="token " * 800 + "tail " * 20),
    ]
    splitter = ChunkSplitterService(max_tokens=800, min_last_chunk=50, overlap=0)
    chunks = list(splitter.split(pages))

    assert len(chunks) == 1
    assert "tail" in chunks[0].content


@pytest.mark.asyncio
async def test_chunk_splitter_emits_final_chunk_when_large_enough():
    pages = [
        PageText(page_number=0, text="token " * 800 + "tail " * 80),
    ]
    splitter = ChunkSplitterService(max_tokens=800, min_last_chunk=50, overlap=0)
    chunks = list(splitter.split(pages))

    assert len(chunks) == 2
    assert "tail" in chunks[1].content


@pytest.mark.asyncio
async def test_chunk_splitter_respects_overlap_tokens():
    text = "try me please " * 800
    pages = [PageText(page_number=0, text=text)]

    splitter = ChunkSplitterService(max_tokens=600, min_last_chunk=100, overlap=100)
    chunks = list(splitter.split(pages))

    assert len(chunks) >= 2
    first_end = splitter.encoding.encode(chunks[0].content)[-100:]
    second_start = splitter.encoding.encode(chunks[1].content)[:100]

    assert first_end == second_start, "Overlap between chunks did not match"


@pytest.mark.asyncio
async def test_chunk_splitter_handles_multiple_pages():
    pages = [
        PageText(page_number=0, text="page one " * 300),
        PageText(page_number=1, text="page two " * 300),
        PageText(page_number=2, text="page three " * 300),
    ]
    splitter = ChunkSplitterService(max_tokens=600, min_last_chunk=50, overlap=50)
    chunks = list(splitter.split(pages))

    text_combined = " ".join(chunk.content for chunk in chunks)
    assert "page one" in text_combined
    assert "page two" in text_combined
    assert "page three" in text_combined
