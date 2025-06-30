from typing import List, Protocol, runtime_checkable
from returns.io import IOResult

from app.protocols.embedding import EmbeddingServiceProtocol
from app.schemas.file_chunk import FileChunkRead


@runtime_checkable
class VectorDBServiceProtocol(Protocol):
    def upsert_chunks(
        self, chunks: List[FileChunkRead], embedding_service: EmbeddingServiceProtocol
    ) -> IOResult[List[List[float]], Exception]:
        """Upsert a chunk into the vector database."""
        ...
