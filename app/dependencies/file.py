from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import FileChunkRepository, FileRepository
from app.dependencies.database import get_db_session
from app.services import FileChunkService, FileService


def get_file_service(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> FileService:
    r = FileRepository(db)
    cr = FileChunkRepository(db)
    return FileService(db, r, cr)
