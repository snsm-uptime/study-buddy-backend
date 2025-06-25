from pathlib import Path
from app.langgraph.state import FileProcessingState
from app.services import ChunkSplitterService

splitter = ChunkSplitterService()


def split_chunks_node(state: FileProcessingState) -> FileProcessingState:
    print(f"[SplitChunks] Splitting chunks for file {state['file_id']}")
    pages = state["pages"]

    file_name = Path(state.get("file_path")).name
    chunks = list(splitter.split(pages, file_name=file_name))
    state["chunks"] = [chunk.content for chunk in chunks]
    state["chunk_metadata"] = chunks  # Optional: retain metadata if needed
    state["step"] = "embed_chunks"
    return state
