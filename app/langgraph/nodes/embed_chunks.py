from app.langgraph.state.file_processing_state import FileProcessingState
from app.protocols.embedding import EmbeddingServiceProtocol
from app.protocols.vector_db import VectorDBServiceProtocol
from app.schemas.file_chunk import PageText
from app.services.chunk_splitter_service import ChunkSplitterService


def build_embed_chunks_node(
    embedding_service: EmbeddingServiceProtocol,
    vector_db_service: VectorDBServiceProtocol,
) -> callable:
    async def embed_chunks_node(state: FileProcessingState) -> FileProcessingState:
        chunks = state["chunks"]
        state["embeddings"] = await vector_db_service.upsert_chunks(
            chunks, embedding_service
        )
        state["step"] = "extract_concepts"
        return state

    return embed_chunks_node
