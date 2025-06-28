from pathlib import Path

from app.langgraph.state import FileProcessingState
from app.services import ChunkSplitterService
from app.services.file_chunk_service import FileChunkService

splitter = ChunkSplitterService()


def build_split_chunks_node(
    file_chunk_service: FileChunkService, chunk_splitter_service: ChunkSplitterService
):
    def split_chunks_node(state: FileProcessingState) -> FileProcessingState:
        chunks = list(
            chunk_splitter_service.split(state["pages"], file_name=state["title"])
        )
        # Create in SQL
        state["chunks"] = chunks
        file_chunk_service.
        state["step"] = "embed_chunks"
        return state

    return split_chunks_node
