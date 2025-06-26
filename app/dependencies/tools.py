from app.services.chunk_splitter_service import ChunkSplitterService


def get_chunk_splitter_service() -> ChunkSplitterService:
    return ChunkSplitterService()
