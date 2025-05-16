import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import SoftDeletableMixin, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.file_chunk import FileChunk
    from app.db.models.user import User


class File(Base, TimestampMixin, SoftDeletableMixin):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", name="fk_files_user_id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str | None] = mapped_column(String, nullable=True)
    source: Mapped[str | None] = mapped_column(Text, nullable=True)
    size_kb: Mapped[float] = mapped_column(Float, nullable=False)

    # Bi-directional relationship
    chunks: Mapped[list["FileChunk"]] = relationship(
        back_populates="file", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship(back_populates="files")
