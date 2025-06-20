import uuid
from sqlite3 import Time
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import SoftDeletableMixin, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.file import File


class FileChunk(Base, SoftDeletableMixin, TimestampMixin):
    __tablename__ = "file_chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("files.id"), nullable=False
    )

    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    end_time: Mapped[float | None] = mapped_column(nullable=True)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    section: Mapped[str] = mapped_column(Text, nullable=True)
    start_time: Mapped[float | None] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    file: Mapped["File"] = relationship(back_populates="chunks")
