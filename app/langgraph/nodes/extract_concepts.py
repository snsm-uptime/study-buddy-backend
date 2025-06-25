from app.langgraph.state.file_processing_state import FileProcessingState


def extract_concepts_node(state: FileProcessingState) -> FileProcessingState:
    print(f"[ExtractConcepts] Extracting concepts for file {state['file_id']}")
    state["concepts"] = ["concept-a", "concept-b"]
    state["step"] = "persist_to_db"
    return state
