from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FileChunkBase(BaseModel):
    chunk_index: int
    section: str | None = None
    text: str


class FileChunkCreate(FileChunkBase):
    file_id: UUID


class FileChunkRead(FileChunkBase):
    id: UUID
    file_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
