from pydantic import BaseModel
from typing import List


class ConceptExtractionResponse(BaseModel):
    concepts: List[str] | None
    domain: str | None
    error: str | None
    minimum_tokens: int | None
    topics: List[str] | None
