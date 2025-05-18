from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from returns.io import IOFailure, IOResult, IOSuccess

from app.dependencies.file import get_file_service
from app.errors import FormValidationError
from app.schemas.file import FileRead
from app.services.file_service import FileService

router = APIRouter()


@router.post("/upload", response_model=FileRead, status_code=status.HTTP_201_CREATED)
async def upload_file(
    service: Annotated[FileService, Depends(get_file_service)],
    author: str = Form(...),
    source: str = Form(...),
    upload: UploadFile = File(...),
    user_id: UUID = Form(...),
) -> FileRead:
    content = await upload.read()
    result = await service.process_and_store_file(
        author=author,
        content=content,
        filename=upload.filename if upload.filename else "Unknown",
        size=upload.size if upload.size else len(content),
        source=source,
        user_id=user_id,
    )
    match result:
        case IOSuccess(file_read):
            return file_read.unwrap()  # type: ignore[no-any-return]
        case IOFailure(err):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=err.failure(),
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
