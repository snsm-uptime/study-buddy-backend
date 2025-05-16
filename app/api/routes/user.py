from typing import Annotated
from uuid import UUID

from httpx import HTTPStatusError
from returns.io import IOSuccess, IOFailure
from fastapi import APIRouter, Depends, HTTPException, status
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
) -> UserRead:
    result = await service.create_user(payload)
    match result:
        case IOSuccess(value):
            return value.unwrap()
        case IOFailure(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(value.failure().args[0]),
            )


@router.get("/", response_model=list[UserRead])
async def get_users(
    service: Annotated[UserService, Depends(get_user_service)],
) -> list[UserRead]:
    result = await service.get_users()
    match result:
        case IOSuccess(values):
            return values.unwrap()
        case IOFailure(value):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(value.failure().args[0]),
            )


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    result = await service.get_user_by_id(user_id)
    match result:
        case IOSuccess(value):
            return value.unwrap()
        case IOFailure(value):
            raise HTTPException(status_code=404, detail=str(value.failure().args[0]))
