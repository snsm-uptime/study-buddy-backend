from app.langgraph.state.file_processing_state import FileProcessingState
from app.protocols.embedding import EmbeddingService
from app.protocols.vector_db import VectorDBService
from app.schemas.file_chunk import PageText
from app.services.chunk_splitter_service import ChunkSplitterService


def build_embed_chunks_node(
    embedding_service: EmbeddingService, vector_db: VectorDBService
):
    def embed_chunks_node(state: FileProcessingState) -> FileProcessingState:
        chunks = state["chunks"]
        vector_db.upsert_chunks(chunks, embedding_service)
        return state

    return embed_chunks_node
