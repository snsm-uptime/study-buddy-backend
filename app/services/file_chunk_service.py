from app.db.repositories.file_chunk_repository import FileChunkRepository


class FileChunkService:
    def __init__(self, repository: FileChunkRepository):
        self.repository = repository
