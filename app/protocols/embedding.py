from typing import List, Protocol, runtime_checkable


@runtime_checkable
class EmbeddingService(Protocol):
    def embed(self, text: str) -> List[float] | None: ...
    def embed_many(self, texts: List[str]) -> List[List[float]]: ...
