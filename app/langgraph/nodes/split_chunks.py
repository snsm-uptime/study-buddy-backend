from app.langgraph.state.file_processing_state import FileProcessingState
from app.schemas.file_chunk import FileChunkBase


def split_chunks_node(state: FileProcessingState) -> FileProcessingState:
    print(f"[SplitChunks] Splitting chunks for file {state['file_id']}")
    state["chunks"] = [
        FileChunkBase(
            content_type="application/text",
            file_name=f"chunk-{i}",
            content=f"Content of chunk {i}",
            page_number=i,
            chunk_index=i,
            section=None,
        )
        for i in range(3)
    ]
    state["step"] = "embed_chunks"
    return state
