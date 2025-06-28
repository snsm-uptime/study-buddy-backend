from app.protocols.embedding import EmbeddingService
from chromadb import Client, Collection
from chromadb.config import Settings
from app.schemas.file_chunk import FileChunkRead
from app.protocols.vector_db import VectorDBService
from app.utils import console
from app.config import get_settings

settings = get_settings()


class ChromaDBService(VectorDBService):
    def __init__(self):
        self.__settings = Settings(
            persist_directory=settings.chroma_persist_directory,
            is_persistent=True,
        )
        self.__client = Client(self.__settings)
        self.__collection = self.__client.get_or_create_collection(
            settings.chroma_collection_name
        )

    @property
    def collection(self) -> Collection:
        return self.__collection

    async def upsert_chunks(
        self, chunks: list[FileChunkRead], embedding_service: EmbeddingService
    ) -> None:
        documents = []
        metadatas = []
        ids = []
        embeddings = []

        for chunk in chunks:
            embedding = embedding_service.embed(chunk)
            if embedding is None:
                console.print(
                    f"[yellow]Skipping chunk {chunk.chunk_index} — no embedding[/yellow]"
                )
                continue

            documents.append(chunk.text)
            embeddings.append(embedding)
            ids.append(chunk.id)
            metadatas.append(chunk.model_dump(exclude={"text"}))

        if documents:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids,
            )
