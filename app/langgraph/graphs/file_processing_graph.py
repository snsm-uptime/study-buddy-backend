from app.langgraph.nodes import (
    parse_file_node,
    split_chunks_node,
    embed_chunks_node,
    extract_concepts_node,
    persist_to_db_node,
)
from langgraph.graph import StateGraph, END

from app.langgraph.state import FileProcessingState


def build_file_processing_graph() -> StateGraph:
    builder = StateGraph(FileProcessingState)

    builder.add_node("parse_file", parse_file_node)
    builder.add_node("split_chunks", split_chunks_node)
    builder.add_node("embed_chunks", embed_chunks_node)
    builder.add_node("extract_concepts", extract_concepts_node)
    builder.add_node("persist_to_db", persist_to_db_node)

    builder.set_entry_point("parse_file")

    builder.add_edge("parse_file", "split_chunks")
    builder.add_edge("split_chunks", "embed_chunks")
    builder.add_edge("embed_chunks", "extract_concepts")
    builder.add_edge("extract_concepts", "persist_to_db")
    builder.add_edge("persist_to_db", END)

    return builder
