from datetime import datetime, timezone
from typing import Iterable, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt


class PageText(BaseModel):
    text: str
    page_number: NonNegativeInt


class TransientChunk(BaseModel):
    text: str
    chunk_index: NonNegativeInt
    start_time: float | None = None
    end_time: float | None = None


class FileChunkBase(TransientChunk):
    file_name: str
    page_numbers: Iterable[NonNegativeInt] | None = None
    sections: Iterable[str] | None = None
    content_type: str | None = None


class FileChunkRead(FileChunkBase):
    id: UUID
    file_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
