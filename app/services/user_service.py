from typing import Optional
from uuid import UUID

from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreate) -> User:
        hashed = hash_password(user_data.password)
        return await self.user_repository.create(
            email=user_data.email, name=user_data.name, hashed_password=hashed
        )

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.get_by_email(email)
