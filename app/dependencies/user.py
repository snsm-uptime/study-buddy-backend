from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user_repository import UserRepository
from app.dependencies.database import get_db_session
from app.services.user_service import UserService


def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)
