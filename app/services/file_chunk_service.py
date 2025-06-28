from typing import List
from app.errors import FormValidationError
from returns.io import IOResult, IOSuccess, IOFailure
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
    ) -> IOResult[List[FileChunkRead], Exception]:
        inserts: List[FileChunk] = [
            FileChunk(
                file_id=file.id,
                page_numbers=chunk.page_numbers,
                file_name=file.title,
                content_type=chunk.content_type,
                chunk_index=chunk.chunk_index,
                sections=chunk.sections,
                text=chunk.text,
            )
            for chunk in chunks
        ]

        return await self.repository.create_many(file_chunks=inserts)

    async def get_by_file_id(
        self, file_id: str
    ) -> IOResult[List[FileChunkRead], Exception]:
        file_chunks_result = await self.repository.get_by_file_id(file_id=file_id)
        match file_chunks_result:
            case IOSuccess(value):
                return IOSuccess(
                    [
                        FileChunkRead.model_validate(chunk, from_attributes=True)
                        for chunk in value.unwrap()
                    ]
                )
            case _:
                IOFailure(
                    FormValidationError(
                        field="upload",
                        message=f"File chunks do not exist. for file {file_id}",
                    )
                )
