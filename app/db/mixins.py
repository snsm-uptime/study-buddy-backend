from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.db.utils import CreatedAt, DeletedAt, UpdatedAt


class TimestampMixin:
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]


class SoftDeletableMixin:
    deleted_at: Mapped[DeletedAt | None] = mapped_column(nullable=True)

    def soft_delete(self) -> None:
        """Marks the instance as deleted without removing from DB."""
        self.deleted_at = datetime.now(timezone.utc)

    def is_deleted(self) -> bool:
        return self.deleted_at is not None
