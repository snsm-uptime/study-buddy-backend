from pathlib import Path
from returns.io import IOSuccess

from app.langgraph.state import FileProcessingState
from app.services import ChunkSplitterService
from app.services.file_chunk_service import FileChunkService
from isort import file

splitter = ChunkSplitterService()


def build_split_chunks_node(
    file_chunk_service: FileChunkService, chunk_splitter_service: ChunkSplitterService
):
    async def split_chunks_node(state: FileProcessingState) -> FileProcessingState:
        chunks = list(
            chunk_splitter_service.split(state["pages"], file_name=state["title"])
        )
        fid = state["file"].id
        state.pop("pages", None)
        # Create in SQL
        await file_chunk_service.create_many(
            file=state["file"],
            chunks=chunks,
        )
        chunks_from_db = await file_chunk_service.get_by_file_id(file_id=fid)
        match chunks_from_db:
            case IOSuccess(value):
                state["chunks"] = value.unwrap()
            case _:
                raise Exception(f"Failed to retrieve file chunks for file_id: {fid}")

        # Create in vector db
        state["step"] = "embed_chunks"
        return state

    return split_chunks_node
