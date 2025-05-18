from returns.io import IOFailure, IOResult, IOSuccess

from app.db.repositories.file_chunk_repository import FileChunkRepository
from app.errors import FormValidationError
from app.schemas.file_chunk import FileChunkCreate, FileChunkRead


class FileChunkService:
    def __init__(self, repository: FileChunkRepository):
        self.repository = repository

    async def create(
        self, chunk: FileChunkCreate
    ) -> IOResult[FileChunkRead, FormValidationError]:
        try:
            result = await self.repository.create(chunk)
            match result:
                case IOSuccess(chunk_data):
                    FileChunkRead.model_validate(chunk_data.unwrap())
                case _:
                    return IOFailure(
                        FormValidationError(
                            field="file_chunk", message="Failed to create file chunk"
                        )
                    )
            return result
        except Exception as e:
            return IOFailure(FormValidationError(field="file_chunk", message=str(e)))
