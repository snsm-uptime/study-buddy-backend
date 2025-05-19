from multiprocessing import Value
from typing import Sequence
from uuid import UUID

from returns.future import future_safe
from returns.io import IOFailure, IOResult, IOSuccess
from returns.result import Failure, Success
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.file import File
from app.db.models.file_chunk import FileChunk
from app.errors import FileNotFoundError
from app.schemas.file_chunk import FileChunkCreate


class FileChunkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @future_safe
    async def create_many(self, file_chunks: list[FileChunk]) -> None:
        try:
            self.session.add_all(file_chunks)
            await self.session.flush()
        except Exception as e:
            raise ValueError(f"Failed to create file chunks: {e}")

    @future_safe
    async def get_all(self) -> Sequence[FileChunk]:
        stmt = select(FileChunk).where(FileChunk.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    @future_safe
    async def get_by_id(self, file_id: UUID) -> FileChunk:
        stmt = select(FileChunk).where(
            FileChunk.id == file_id, FileChunk.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        file = result.scalar_one_or_none()
        if not file:
            raise FileNotFoundError(str(file_id))
        return file

    @future_safe
    async def get_by_file_id(self, file_id: UUID) -> Sequence[FileChunk]:
        stmt = select(FileChunk).where(
            FileChunk.file_id == file_id, FileChunk.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    @future_safe
    async def soft_delete(self, file_id: UUID) -> bool:
        result = await self.get_by_id(file_id)
        match result:
            case IOSuccess(file):
                async with self.session.begin():
                    file.unwrap().soft_delete()
                return True
            case _:
                return False
