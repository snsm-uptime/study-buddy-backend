from app.protocols.embedding import EmbeddingServiceProtocol
from app.protocols.parser import FileParserProtocol
from app.protocols.vector_db import VectorDBServiceProtocol
from app.services.chunk_splitter_service import ChunkSplitterService
from app.services.file_chunk_service import FileChunkService
from app.services.file_service import FileService
from app.services.llm.llm_service import LLMService
from app.services.parsers.pdf_parser import PDFPlumberParser
from app.services.user_service import UserService
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.langgraph.nodes import (
    build_embed_chunks_node,
    build_extract_concepts_node,
    build_parse_file_node,
    build_persist_to_db_node,
    build_split_chunks_node,
)
from app.langgraph.state import FileProcessingState


def build_file_processing_graph(
    # user_service: UserService,
    chunk_splitter_service: ChunkSplitterService,
    embedding_service: EmbeddingServiceProtocol,
    file_chunk_service: FileChunkService,
    file_service: FileService,
    pdf_parser: FileParserProtocol,
    vector_db_service: VectorDBServiceProtocol,
) -> CompiledStateGraph:
    builder = StateGraph(FileProcessingState)

    builder.add_node(
        "parse_file",
        build_parse_file_node(file_service=file_service, parser=pdf_parser),
    )
    builder.add_node(
        "split_chunks",
        build_split_chunks_node(
            file_chunk_service=file_chunk_service,
            chunk_splitter_service=chunk_splitter_service,
        ),
    )
    builder.add_node(
        "embed_chunks",
        build_embed_chunks_node(
            embedding_service=embedding_service, vector_db_service=vector_db_service
        ),
    )
    builder.add_node(
        "extract_concepts",
        build_extract_concepts_node(llm_service=LLMService()),
    )
    builder.add_node("persist_to_db", build_persist_to_db_node)

    builder.set_entry_point("parse_file")

    # Single dynamic router
    builder.add_conditional_edges("parse_file", lambda state: state["step"])
    builder.add_conditional_edges("split_chunks", lambda state: state["step"])
    builder.add_conditional_edges("embed_chunks", lambda state: state["step"])
    builder.add_conditional_edges("extract_concepts", lambda state: state["step"])
    builder.add_conditional_edges("persist_to_db", lambda state: state["step"])

    return builder.compile()
