from app.protocols.embedding import EmbeddingServiceProtocol
from app.services.chunk_splitter_service import ChunkSplitterService
from app.services.embedding.sentence_transformer import (
    SentenceTransformerEmbeddingService,
)
from sentence_transformers import SentenceTransformer


async def get_chunk_splitter_service() -> ChunkSplitterService:
    return ChunkSplitterService()  # TODO: does this need a singleton pattern?


_embedding_service_instance: EmbeddingServiceProtocol | None = None


async def get_embedding_service() -> EmbeddingServiceProtocol:
    global _embedding_service_instance
    if _embedding_service_instance is None:
        _embedding_service_instance = SentenceTransformerEmbeddingService()
    return _embedding_service_instance
