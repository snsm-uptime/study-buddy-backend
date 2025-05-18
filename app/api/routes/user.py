from typing import Annotated, List, Optional, Sequence, cast
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from httpx import HTTPStatusError
from returns.io import IOFailure, IOSuccess
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user_repository import UserRepository
from app.dependencies.database import get_db_session
from app.dependencies.user import get_user_service
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> Optional[UserRead]:
    result = await service.create_user(payload)
    match result:
        case IOSuccess(value):
            return cast(UserRead, value.unwrap())
        case IOFailure(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(value.failure().args[0]),
            )
    return None


@router.get("/", response_model=Sequence[UserRead])
async def get_users(
    service: Annotated[UserService, Depends(get_user_service)],
) -> List[UserRead]:
    result = await service.get_users()
    match result:
        case IOSuccess(values):
            return cast(List[UserRead], values.unwrap())
        case IOFailure(value):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(value.failure().args[0]),
            )
    return []


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> Optional[UserRead]:
    result = await service.get_user_by_id(user_id)
    match result:
        case IOSuccess(value):
            return cast(UserRead, value.unwrap())
        case IOFailure(value):
            raise HTTPException(status_code=404, detail=str(value.failure().args[0]))
    return None
