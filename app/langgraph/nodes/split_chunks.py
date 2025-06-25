from app.langgraph.state.file_processing_state import FileProcessingState


def split_chunks_node(state: FileProcessingState) -> FileProcessingState:
    print(f"[SplitChunks] Splitting chunks for file {state['file_id']}")
    state["chunks"] = [f"chunk-{i}" for i in range(3)]
    state["step"] = "embed_chunks"
    return state
