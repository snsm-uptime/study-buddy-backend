from typing import Any, List, Mapping

import chromadb
from chromadb.api import ClientAPI
from chromadb.config import Settings

from app.protocols.vector_db import VectorDBService
from app.config import get_settings


class ChromaDBVectorService(VectorDBService):
    def __init__(self):
        app_settings = get_settings()
        self.client: ClientAPI = chromadb.Client(
            Settings(persist_directory=app_settings.chroma_persist_directory)
        )
        self.collection = self.client.get_or_create_collection(
            name=app_settings.chroma_collection_name
        )

    def get_embedding(self, text: str) -> List[float] | None:
        # Replace with your actual embedding logic or model call
        from app.services.embedding import embed_text

        return embed_text(text)

    def add_embedding(
        self,
        vector_id: str,
        embedding: List[float],
        document: str,
        metadata: Mapping[str, Any],
    ) -> None:
        self.collection.add(
            ids=[vector_id],
            embeddings=[embedding],
            documents=[document],
            metadatas=[metadata],
        )
