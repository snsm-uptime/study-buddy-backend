from datetime import datetime
from typing import Any, List
from uuid import UUID
from returns.io import IOResult
from app.protocols.embedding import EmbeddingServiceProtocol
from chromadb import Client, Collection
from chromadb.config import Settings
from app.schemas.file_chunk import FileChunkRead
from app.protocols.vector_db import VectorDBServiceProtocol
from app.config import get_settings

settings = get_settings()


class ChromaDBService(VectorDBServiceProtocol):
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
        self, chunks: list[FileChunkRead], embedding_service: EmbeddingServiceProtocol
    ) -> IOResult[List[List[float]], Exception]:
        def normalize_metadata(chunk: FileChunkRead) -> dict[str, Any]:
            raw = chunk.model_dump()

            def to_scalar(value: Any) -> Any:
                if isinstance(value, (str, int, float, bool)) or value is None:
                    return value
                if isinstance(value, list):
                    return ",".join(map(str, value))
                if isinstance(value, UUID):
                    return str(value)
                if isinstance(value, datetime):
                    return value.isoformat()

            return {k: to_scalar(v) for k, v in raw.items() if v is not None}

        documents = []
        metadatas = []
        ids = []
        embeddings = []

        for chunk in chunks:
            embedding = embedding_service.embed(chunk.text)
            if embedding is None:
                continue

            documents.append(chunk.text)
            embeddings.append(embedding)
            ids.append(str(chunk.id))
            metadatas.append(normalize_metadata(chunk))

        if documents:
            self.collection.upsert(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids,
            )
            return IOResult.from_value(embeddings)
        else:
            raise ValueError("No valid chunks to upsert.")
