import asyncio
from typing import Sequence
from uuid import UUID

from returns.io import IOFailure, IOResult, IOSuccess
from returns.iterables import Fold

from app.db.repositories.file_repository import FileRepository
from app.errors import FileNotFoundError, FormValidationError
from app.schemas.file import FileCreate, FileRead
from app.schemas.file_chunk import FileChunkCreate
from app.services.file_chunk_service import FileChunkService
from app.utils.text import split_text_into_chunks


class FileService:
    def __init__(
        self, file_repository: FileRepository, file_chunk_service: FileChunkService
    ):
        self.file_chunk_service = file_chunk_service
        self.file_repository = file_repository

    async def process_and_store_file(
        self,
        *,
        filename: str,
        size: int,
        content: bytes,
        user_id: UUID,
        author: str,
        source: str,
    ) -> IOResult[FileRead, FormValidationError]:
        try:
            decoded_text = content.decode("utf-8")  # support only utf-8 for now
            chunks = split_text_into_chunks(decoded_text, chunk_size=500)

            file_create = FileCreate(
                title=filename,
                author=author,
                size_bytes=size,
                source=source,
                user_id=user_id,
            )

            # Upload the file metadata
            file_result = await self.upload_file(file_create)

            match file_result:
                case IOSuccess(file_data):
                    file = file_data.unwrap()
                    create_batch = []
                    for index, chunk in enumerate(chunks):
                        fc = FileChunkCreate(
                            file_id=file.id,
                            chunk_index=index,
                            section=None,
                            text=chunk,
                        )
                        # TODO: Each chunk analyze if there's a section it can be grouped into.
                        create_batch.append(self.file_chunk_service.create(fc))
                    await asyncio.gather(*create_batch)
                    return IOSuccess.from_result(file_data)
                case _:
                    return file_result
        except Exception as e:
            return IOFailure(FormValidationError(field="file", message=str(e)))

    async def upload_file(
        self, file_data: FileCreate
    ) -> IOResult[FileRead, FormValidationError]:
        # Check if the file already exists for the user
        existing_result = await self.file_repository.get_by_user_and_title_size(
            user_id=file_data.user_id,
            title=file_data.title,
            size_bytes=file_data.size_bytes,
        )

        match existing_result:
            case IOSuccess(_):
                return IOFailure(
                    FormValidationError(
                        field="file", message="This file has already been uploaded."
                    )
                )
            case _:
                result = await self.file_repository.create(**file_data.model_dump())
                match result:
                    case IOSuccess(f):
                        return IOSuccess(FileRead.model_validate(f.unwrap()))
                    case _:
                        return IOFailure(
                            FormValidationError(
                                field="file", message="Failed to upload file"
                            )
                        )

    async def get_file_by_id(
        self, file_id: UUID
    ) -> IOResult[FileRead, FileNotFoundError]:
        result = await self.file_repository.get_by_id(file_id)
        match result:
            case IOSuccess(value):
                return IOSuccess(
                    FileRead.model_validate(value.unwrap(), from_attributes=True)
                )
            case _:
                return IOFailure(FileNotFoundError(identifier=str(file_id)))

    async def get_files_by_user(
        self, user_id: UUID
    ) -> IOResult[list[FileRead], FileNotFoundError]:
        result = await self.file_repository.get_by_user_id(user_id)
        match result:
            case IOSuccess(files):
                return IOSuccess(
                    [
                        FileRead.model_validate(f, from_attributes=True)
                        for f in files.unwrap()
                    ]
                )
            case _:
                return IOFailure(FileNotFoundError(identifier=str(user_id)))

    async def delete_file(self, file_id: UUID) -> IOResult[bool, FileNotFoundError]:
        result = await self.file_repository.soft_delete(file_id)
        match result:
            case IOSuccess(_):
                return IOSuccess(True)
            case _:
                return IOFailure(FileNotFoundError(identifier=str(file_id)))
