from app.services.vector_db.chroma import ChromaDBService
from chromadb import Client, Collection
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


_chromadb_instance = None


def get_chromadb():
    global _chromadb_instance
    if _chromadb_instance is None:
        _chromadb_instance = ChromaDBService()
    return _chromadb_instance
