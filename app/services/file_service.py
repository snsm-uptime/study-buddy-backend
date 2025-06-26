from math import e
from uuid import UUID

from app.langgraph.state.file_processing_state import FileProcessingState
from app.services.file_chunk_service import FileChunkService
from returns.io import IOFailure, IOResult, IOSuccess
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.file import File
from app.db.models.file_chunk import FileChunk
from app.db.repositories.file_chunk_repository import FileChunkRepository
from app.db.repositories.file_repository import FileRepository
from app.errors import FileNotFoundError, FormValidationError
from app.schemas.file import FileCreate, FileRead
from app.utils.text import split_text_into_chunks


class FileService:
    def __init__(
        self,
        session: AsyncSession,
        file_repository: FileRepository,
        file_chunk_service: FileChunkService,
    ):
        self.session = session
        self.file_chunk_service = file_chunk_service
        self.file_repository = file_repository

    async def check_file_exists(
        self, user_id: UUID, filename: str, size_bytes: float
    ) -> bool:
        # Validate if file exists in database
        existing_result = await self.file_repository.get_by_user_and_title_size(
            user_id=user_id,
            title=filename,
            size_bytes=size_bytes,
        )
        return isinstance(existing_result, IOFailure)

    async def upload_and_process_file(
        self,
        user_id: UUID,
        filename: str,
        content: bytes,
        size_bytes: float,
        author: str = "",
        source: str = "file",
    ) -> IOResult[FileRead, FormValidationError]:
        decoded_text = content.decode("utf-8")
        async with self.session.begin():
            # Create file entry in the database
            file_create_response = await self.file_repository.create(
                user_id=user_id,
                title=filename,
                size_bytes=size_bytes,
                author=author,
                source=source,
            )
            match file_create_response:
                case IOSuccess(file_data):
                    file: File = file_data.unwrap()
                    # file_chunks = [
                    #     FileChunk(
                    #         file_id=file.id,
                    #         chunk_index=index,
                    #         section=None,
                    #         text=chunk,
                    #     )
                    #     for index, chunk in enumerate(chunks)
                    # ]
                    # res = await self.file_chunk_repository.create_many(file_chunks)
                    # match res:
                    #     case IOSuccess(_):
                    #         return IOSuccess(FileRead.model_validate(file))
                    #     case _:
                    #         return IOFailure(
                    #             FormValidationError(
                    #                 field="file_chunks",
                    #                 message="Failed to persist file chunks",
                    #             )
                    #         )
                case IOFailure(exception):
                    err = exception.failure()
                    failure: FormValidationError
                    if isinstance(err, IntegrityError):
                        failure = FormValidationError(
                            field="file",
                            message=f"[FAIL:FILE] {err.params} {err.args[0]}",
                        )
                    return IOFailure(failure)
                case _:
                    return IOFailure(
                        FormValidationError(
                            field="file", message=f"Failed to upload file"
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
