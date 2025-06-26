from app.langgraph.state.file_processing_state import FileProcessingState
from app.schemas.file_chunk import PageText
from app.services.chunk_splitter_service import ChunkSplitterService


def build_embed_chunks_node(chunk_splitter_service: ChunkSplitterService):
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

    return embed_chunks_node
