from typing import Sequence
from uuid import UUID

from returns.future import future_safe
from returns.io import IOFailure, IOResult, IOSuccess
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.file import File
from app.errors import FileNotFoundError


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @future_safe
    async def create(
        self,
        *,
        user_id: UUID,
        title: str,
        size_bytes: float,
        author: str = "",
        source: str = "",
    ) -> File:
        file = File(
            user_id=user_id,
            title=title,
            size_bytes=size_bytes,
            author=author,
            source=source,
        )
        self.session.add(file)
        await self.session.flush()
        await self.session.refresh(file)
        return file

    @future_safe
    async def get_all(self) -> Sequence[File]:
        stmt = select(File).where(File.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    @future_safe
    async def get_by_id(self, file_id: UUID) -> File:
        stmt = select(File).where(File.id == file_id, File.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        file = result.scalar_one_or_none()
        if not file:
            raise FileNotFoundError(str(file_id))
        return file

    @future_safe
    async def get_by_user_id(self, user_id: UUID) -> Sequence[File]:
        stmt = select(File).where(File.user_id == user_id, File.deleted_at.is_(None))
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

    @future_safe
    async def get_by_user_and_title_size(
        self, user_id: UUID, title: str, size_bytes: float
    ) -> File:
        stmt = select(File).where(
            File.user_id == user_id,
            File.title == title,
            File.size_bytes == size_bytes,
        )
        result = await self.session.execute(stmt)
        file = result.scalar_one()
        return file
