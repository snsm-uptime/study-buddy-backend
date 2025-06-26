from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    author: str
    size_bytes: float
    content_type: str
    title: str


class FileCreate(FileBase):
    user_id: UUID


class FileRead(FileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
