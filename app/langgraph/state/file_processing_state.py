from typing import Any, BinaryIO, List, Literal, TypedDict
from uuid import UUID

from app.schemas.file_chunk import FileChunkRead, PageText


class FileProcessingState(TypedDict, total=False):
    author: str
    chunks: List[FileChunkRead]
    concepts: List[str]
    content_type: str
    embeddings: List[str]
    file_buffer: BinaryIO
    file: FileChunkRead
    title: str
    pages: List[PageText]
    parsed: bool
    saved: bool
    size_bytes: float
    user_id: str
    step: Literal[
        "parse_file",
        "split_chunks",
        "embed_chunks",
        "extract_concepts",
        "persist_to_db",
        "done",
    ] = "parse_file"
