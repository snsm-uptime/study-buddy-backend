from typing import List
from app.db.models.file_chunk import FileChunk
from app.db.repositories.file_chunk_repository import FileChunkRepository
from app.schemas.file import FileRead
from app.schemas.file_chunk import FileChunkBase, FileChunkRead, PageText


class FileChunkService:
    def __init__(self, repository: FileChunkRepository):
        self.repository = repository

    async def create_many(
        self,
        file: FileRead,
        chunks: List[FileChunkBase],
    ) -> List[FileChunkRead]:
        inserts: List[FileChunk] = [
            FileChunk(
                file_id=file.id,
                page_number=chunk.page_number,
                text=chunk.text,
                metadata=chunk.metadata or {},
            )
            for chunk in chunks
        ]

        return await self.repository.create_many(file=file, pages=chunks)
