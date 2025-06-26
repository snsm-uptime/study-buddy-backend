from typing import Any, List, Mapping, Protocol, runtime_checkable

from app.schemas.file_chunk import FileChunkBase


@runtime_checkable
class VectorDBService(Protocol):
    def upsert_chunks(
        self,
        file_id: str,
        file_name: str,
        embeddings: List[List[float]],
        chunks: List[FileChunkBase],
    ) -> None:
        """Upsert a chunk into the vector database."""

    def query_similar(text: str, top_k: int) -> List[str]: ...
