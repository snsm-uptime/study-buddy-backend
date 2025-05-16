from re import U
from typing import List, Optional
from unittest import result
from uuid import UUID

from app.api.routes.user import IOFailure, IOSuccess
from fastapi import Form
from returns.future import FutureResult
from returns.io import IOResult
from returns.result import Failure, Result, Success

from app.api.errors import UserNotFoundError, NoItemsFoundError, FormValidationError
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.utils.security import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(
        self, user_data: UserCreate
    ) -> IOResult[User, FormValidationError]:
        existing = await self.user_repository.get_by_email(user_data.email)
        if isinstance(existing, IOSuccess):
            return IOFailure(
                FormValidationError(
                    field="email",
                    message="Email already registered",
                )
            )

        hashed = hash_password(user_data.password)
        created_user_response = await self.user_repository.create(
            email=user_data.email, name=user_data.name, hashed_password=hashed
        )
        match created_user_response:
            case IOSuccess(value):
                return IOSuccess(
                    UserRead.model_validate(value.unwrap(), from_attributes=True)
                )
            case IOFailure(value):
                raise IOFailure(
                    FormValidationError(
                        field="email",
                        message=value.failure().args[0],
                    )
                )

    async def get_users(self) -> IOResult[List[User], NoItemsFoundError]:
        result = await self.user_repository.get_all()
        match result:
            case IOSuccess(value):
                return IOSuccess(
                    [
                        UserRead.model_validate(u, from_attributes=True)
                        for u in value.unwrap()
                    ]
                )
            case IOFailure(value):
                return IOFailure(NoItemsFoundError(query=value.failure().args[0]))

    async def get_user_by_id(self, user_id: UUID) -> IOResult[User, UserNotFoundError]:
        result = await self.user_repository.get_by_id(user_id)
        match result:
            case IOSuccess(value):
                return IOSuccess(
                    UserRead.model_validate(value.unwrap(), from_attributes=True)
                )
            case IOFailure(value):
                return IOFailure(UserNotFoundError(identifier=user_id))

    async def get_user_by_email(self, email: str) -> IOResult[User, UserNotFoundError]:
        result = await self.user_repository.get_by_email(email)
        match result:
            case IOSuccess(value):
                return IOSuccess(
                    UserRead.model_validate(value.unwrap(), from_attributes=True)
                )
            case IOFailure(value):
                return IOFailure(UserNotFoundError(identifier=email))
