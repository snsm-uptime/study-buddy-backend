from typing import List, Literal, TypedDict
from uuid import UUID

from app.schemas.file_chunk import FileChunkBase, PageText


class FileProcessingState(TypedDict, total=False):
    file_id: UUID
    file_path: str
    parsed: bool
    chunks: List[FileChunkBase]
    pages: List[PageText]
    concepts: List[str]
    saved: bool
    step: Literal[
        "parse_file",
        "split_chunks",
        "embed_chunks",
        "extract_concepts",
        "persist_to_db",
        "done",
    ]
