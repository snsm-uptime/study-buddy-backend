from math import e
from typing import IO, Annotated
from uuid import UUID

from app.langgraph.state.file_processing_state import FileProcessingState
from app.protocols.embedding import EmbeddingServiceProtocol
from app.services.parsers.pdf_parser import PDFPlumberParser
from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.dependencies import (
    get_file_service,
    get_chunk_splitter_service,
    get_file_chunk_service,
    get_vector_db_service,
    get_embedding_service,
)
from app.errors import FormValidationError
from app.schemas.file import FileRead
from app.services.file_service import FileService
from app.langgraph.graphs.file_processing_graph import build_file_processing_graph
from isort import file

router = APIRouter()


@router.post("/upload", response_model=FileRead, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file_service: Annotated[FileService, Depends(get_file_service)],
    file_chunk_service: Annotated[FileService, Depends(get_file_chunk_service)],
    chunk_splitter_service: Annotated[FileService, Depends(get_chunk_splitter_service)],
    vector_db_service: Annotated[FileService, Depends(get_vector_db_service)],
    embedding_service: Annotated[
        EmbeddingServiceProtocol, Depends(get_embedding_service)
    ],
    author: str = Form(...),
    source: str = Form(...),
    upload: UploadFile = File(...),
    user_id: UUID = Form(...),
) -> str:

    state = FileProcessingState(
        author=author,
        content_type=upload.content_type,
        file_buffer=upload.file,
        filename=upload.filename if upload.filename else "Unknown",
        size_bytes=upload.size,
        source=source,
        title=upload.filename,
        user_id=user_id,
    )
    graph = build_file_processing_graph(
        chunk_splitter_service=chunk_splitter_service,
        embedding_service=embedding_service,
        file_chunk_service=file_chunk_service,
        file_service=file_service,
        pdf_parser=PDFPlumberParser(),
        vector_db_service=vector_db_service,
    )
    file_processing_result = await graph.ainvoke(state)
    return file_processing_result["state"].file_id
    # match result:
    #     case IOSuccess(file_read):
    #         return file_read.unwrap()  # type: ignore[no-any-return]
    #     case IOFailure(err):
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #             detail=err.failure().args[0],
    #         )
    #     case _:
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         )
