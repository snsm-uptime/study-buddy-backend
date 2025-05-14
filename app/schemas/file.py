from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FileUploadResponse(BaseModel):
    id: UUID
    title: str
    author: str | None = None
    source: str | None = None
    size_kb: float
    uploaded_at: datetime

    class Config:
        orm_mode = True
