import tiktoken
from typing import Iterator, List
from app.schemas.file_chunk import ChunkData, PageText
from app.config import get_settings


class ChunkSplitterService:
    def __init__(
        self,
        model_name: str = get_settings().tiktoken_model,
        max_tokens: int = get_settings().max_tokens,
        min_last_chunk: int = get_settings().min_last_chunk,
        overlap: int = get_settings().overlap_tokens,
    ):
        self.encoding = tiktoken.get_encoding(model_name)
        self.max_tokens = max_tokens
        self.min_last_chunk = min_last_chunk
        self.overlap = overlap

    def split(self, pages: List[PageText]) -> Iterator[ChunkData]:
        token_buffer: list[int] = []
        page_map: list[int] = []
        chunk_index = 0

        for page in pages:
            page_tokens = self.encoding.encode(page.text)
            token_buffer.extend(page_tokens)
            page_map.extend([page.page_number] * len(page_tokens))

            while len(token_buffer) >= self.max_tokens + self.min_last_chunk:
                chunk_tokens = token_buffer[: self.max_tokens]
                chunk_text = self.encoding.decode(chunk_tokens)
                page_number = page_map[0]

                yield ChunkData(
                    content=chunk_text,
                    chunk_index=chunk_index,
                    page_number=page_number,
                    section=None,
                )
                chunk_index += 1

                # Retain overlap
                token_buffer = token_buffer[self.max_tokens - self.overlap :]
                page_map = page_map[self.max_tokens - self.overlap :]

        # Final chunk — merge remaining into one
        if token_buffer:
            chunk_text = self.encoding.decode(token_buffer)
            page_number = page_map[0]

            yield ChunkData(
                content=chunk_text,
                chunk_index=chunk_index,
                page_number=page_number,
                section=None,
            )
