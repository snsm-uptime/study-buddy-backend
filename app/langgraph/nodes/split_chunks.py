from pathlib import Path

from app.langgraph.state import FileProcessingState
from app.services import ChunkSplitterService

splitter = ChunkSplitterService()


def build_split_chunks_node(chunk_splitter_service: ChunkSplitterService):
    def split_chunks_node(state: FileProcessingState) -> FileProcessingState:
        chunks = list(
            chunk_splitter_service.split(state["pages"], file_name=state["title"])
        )
        state["chunks"] = chunks
        # state["chunk_metadata"] = chunks  # Optional: retain metadata if needed
        state["step"] = "embed_chunks"
        return state

    return split_chunks_node
