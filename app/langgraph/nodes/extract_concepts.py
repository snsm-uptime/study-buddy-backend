from app.langgraph.state.file_processing_state import FileProcessingState


def build_extract_concepts_node(state: FileProcessingState) -> FileProcessingState:
    print(f"[ExtractConcepts] Extracting concepts for file {state['file'].id}")
    state["concepts"] = ["concept-a", "concept-b"]
    state["step"] = "persist_to_db"
    return state
