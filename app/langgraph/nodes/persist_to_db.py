from app.langgraph.state.file_processing_state import FileProcessingState


def build_persist_to_db_node(state: FileProcessingState) -> FileProcessingState:
    state["saved"] = True
    state["step"] = "done"
    return state
