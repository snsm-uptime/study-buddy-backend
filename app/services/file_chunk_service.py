from app.db.repositories.file_chunk_repository import FileChunkRepository
from app.schemas.file import FileRead
from app.schemas.file_chunk import PageText


class FileChunkService:
    def __init__(self, repository: FileChunkRepository):
        self.repository = repository

    # async def process_pages(
    #         self,
    #         file: FileRead,
    #         pages: List[PageText]
    # )
