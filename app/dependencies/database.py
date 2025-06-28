from typing import AsyncGenerator

from app.protocols.vector_db import VectorDBServiceProtocol
from app.services.vector_db.chroma import ChromaDBService
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


_chromadb_instance: ChromaDBService | None = None


async def get_vector_db_service() -> VectorDBServiceProtocol:
    global _chromadb_instance
    if _chromadb_instance is None:
        _chromadb_instance = ChromaDBService()
    return _chromadb_instance
