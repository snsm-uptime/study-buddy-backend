from typing import List, Protocol, runtime_checkable

from app.protocols.embedding import EmbeddingService
from app.schemas.file_chunk import FileChunkBase


@runtime_checkable
class VectorDBService(Protocol):
    def upsert_chunks(
        self, chunks: List[FileChunkBase], embedding_service: EmbeddingService
    ) -> None:
        """Upsert a chunk into the vector database."""
        ...
