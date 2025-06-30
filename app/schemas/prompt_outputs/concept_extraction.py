from pydantic import BaseModel
from typing import List


class ConceptExtractionResponse(BaseModel):
    domain: str | None
    concepts: List[str] | None
    topics: List[str] | None
    error: str | None
    minimum_tokens: int | None
