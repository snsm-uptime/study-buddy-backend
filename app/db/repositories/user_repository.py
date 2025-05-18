import uuid
from datetime import datetime, timezone
from typing import Sequence

from returns.future import future_safe
from returns.io import IOFailure, IOSuccess
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.errors import NoItemsFoundError, UserNotFoundError


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @future_safe
    async def get_all(self) -> Sequence[User]:
        stmt = select(User).where(User.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        try:
            users = list(result.scalars().all())
        except Exception as e:
            raise NoItemsFoundError(str(e))
        return users

    @future_safe
    async def get_by_id(self, user_id: uuid.UUID) -> User:
        stmt = select(User).where(User.id == user_id, User.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFoundError(str(user_id))
        return user

    @future_safe
    async def get_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email, User.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFoundError(email)
        return user

    @future_safe
    async def create(self, *, email: str, name: str, hashed_password: str) -> User:
        user = User(email=email, name=name, password=hashed_password)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        await self.session.commit()
        return user

    async def soft_delete(self, user_id: uuid.UUID) -> bool:
        result = await self.get_by_id(user_id)
        match result:
            case IOSuccess(user):
                user.unwrap().soft_delete()
                await self.session.flush()
                await self.session.commit()
                return True
            case _:
                return False
