from app.langgraph.state.file_processing_state import FileProcessingState


def persist_to_db_node(state: FileProcessingState) -> FileProcessingState:
    print(f"[PersistToDB] Saving data for file {state['file_id']}")
    state["saved"] = True
    state["step"] = "done"
    return state
