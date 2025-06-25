from app.langgraph.state.file_processing_state import FileProcessingState
from app.schemas.file_chunk import PageText


def embed_chunks_node(state: FileProcessingState) -> FileProcessingState:
    print(f"[EmbedChunks] Embedding chunks for file {state['file_id']}")
    state["embeddings"] = [
        PageText(
            text=f"embedding-{i.content}",
            page_number=i.page_number if i.page_number is not None else 0,
        )
        for i in state["chunks"]
    ]
    state["step"] = "extract_concepts"
    return state
