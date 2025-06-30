from typing import Iterator, List

import tiktoken

from app.config import get_settings
from app.schemas.file_chunk import FileChunkBase, PageText


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

    def split(self, pages: List[PageText], file_name: str) -> Iterator[FileChunkBase]:
        token_buffer: list[int] = []
        page_map: list[int] = []
        chunk_index = 0

        for page in pages:
            page_tokens = self.encoding.encode(page.text)
            token_buffer.extend(page_tokens)
            # list of page numbers corresponding to the tokens in the buffer
            page_map.extend([page.page_number] * len(page_tokens))
            while len(token_buffer) >= self.max_tokens + self.min_last_chunk:
                chunk_tokens = token_buffer[: self.max_tokens]
                # Here the tokens are sliced to the max_tokens limit
                # They are then parsed to text again
                chunk_text = self.encoding.decode(chunk_tokens)
                page_numbers = set(page_map[: self.max_tokens])

                yield FileChunkBase(
                    text=chunk_text,
                    chunk_index=chunk_index,
                    page_numbers=list(page_numbers),
                    section=None,
                    file_name=file_name,
                )
                chunk_index += 1

                # Retain overlap
                token_buffer = token_buffer[self.max_tokens - self.overlap :]
                page_map = page_map[self.max_tokens - self.overlap :]

        if token_buffer:
            chunk_text = self.encoding.decode(token_buffer)
            page_numbers = set(page_map)

            yield FileChunkBase(
                text=chunk_text,
                chunk_index=chunk_index,
                page_numbers=page_numbers,
                file_name=file_name,
            )
