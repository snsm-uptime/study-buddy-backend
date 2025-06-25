from app.langgraph.state.file_processing_state import FileProcessingState


def embed_chunks_node(state: FileProcessingState) -> FileProcessingState:
    print(f"[EmbedChunks] Embedding chunks for file {state['file_id']}")
    state["embeddings"] = [f"embedding-{i}" for i in range(len(state["chunks"]))]
    state["step"] = "extract_concepts"
    return state
