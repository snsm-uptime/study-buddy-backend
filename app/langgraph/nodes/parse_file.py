from app.langgraph.state.file_processing_state import FileProcessingState


def parse_file_node(state: FileProcessingState) -> FileProcessingState:
    print(f"[ParseFile] Processing file {state['file_id']}")
    state["parsed"] = True
    state["step"] = "split_chunks"
    return state
