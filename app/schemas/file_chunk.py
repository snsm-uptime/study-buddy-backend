from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt


class PageText(BaseModel):
    text: str
    page_number: NonNegativeInt


class TransientChunk(BaseModel):
    content: str
    chunk_index: NonNegativeInt
    start_time: float | None = None
    end_time: float | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FileChunkBase(TransientChunk):
    file_name: str
    page_number: NonNegativeInt | None = None
    section: str | None = None
    content_type: str | None = None


class FileChunkRead(FileChunkBase):
    id: UUID
    file_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
