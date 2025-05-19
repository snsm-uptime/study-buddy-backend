from returns.io import IOFailure, IOResult, IOSuccess

from app.db.repositories.file_chunk_repository import FileChunkRepository
from app.errors import FormValidationError
from app.schemas.file_chunk import FileChunkCreate, FileChunkRead


class FileChunkService:
    def __init__(self, repository: FileChunkRepository):
        self.repository = repository
