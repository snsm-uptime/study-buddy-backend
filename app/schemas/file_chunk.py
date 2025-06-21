from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


# Transient use in LangGraph pipeline
class ChunkData(BaseModel):
    content: str
    chunk_index: int
    section: str | None = None
    page_number: int | None = None
    start_time: float | None = None
    end_time: float | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FileChunkBase(BaseModel):
    chunk_index: int
    content_type: str | None = None
    end_time: float | None = None
    page_number: int | None = None
    section: str | None = None
    start_time: float | None = None
    content: str


class FileChunkCreate(FileChunkBase):
    file_id: UUID


class FileChunkRead(FileChunkBase):
    id: UUID
    file_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
