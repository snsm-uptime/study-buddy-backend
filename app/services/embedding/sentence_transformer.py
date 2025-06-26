from sentence_transformers import SentenceTransformer
from typing import List
from app.protocols import EmbeddingService


class SentenceTransformerEmbeddingService(EmbeddingService):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> List[float] | None:
        return self.model.encode(text, convert_to_numpy=True).tolist()
