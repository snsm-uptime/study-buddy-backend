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
        fid = state["file"].id
        check_db_result = await file_chunk_service.get_by_file_id(file_id=fid)
        match check_db_result:
            case IOSuccess(value):
                state["chunks"] = value.unwrap()
            case _:
                chunks = list(
                    chunk_splitter_service.split(
                        state["pages"], file_name=state["title"]
                    )
                )
                state.pop("pages", None)
                # Create in SQL
                await file_chunk_service.create_many(
                    file=state["file"],
                    chunks=chunks,
                )
                check_result = await file_chunk_service.get_by_file_id(file_id=fid)
                match check_result:
                    case IOSuccess(value):
                        state["chunks"] = value.unwrap()
                    case _:
                        raise Exception(
                            f"Failed to retrieve file chunks for file_id: {fid}"
                        )
        state["step"] = "embed_chunks"
        return state

    return split_chunks_node
