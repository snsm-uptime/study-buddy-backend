from email import message
from typing import List, Sequence
from uuid import UUID

from returns.io import IOFailure, IOResult, IOSuccess

from app.db.repositories.user_repository import UserRepository
from app.errors import FormValidationError, NoItemsFoundError, UserNotFoundError
from app.schemas.user import UserCreate, UserRead
from app.utils.security import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(
        self, user_data: UserCreate
    ) -> IOResult[UserRead, FormValidationError]:
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
                return IOSuccess(UserRead.model_validate(value.unwrap()))
            case IOFailure(value):
                return IOFailure(
                    FormValidationError(
                        field="email",
                        message=str(value.failure().args[0]),
                    )
                )
            case _:
                return IOFailure(
                    FormValidationError(
                        field="email",
                        message="Unknown Error occurred while creating user",
                    )
                )

    async def get_users(self) -> IOResult[Sequence[UserRead], NoItemsFoundError]:
        result = await self.user_repository.get_all()
        match result:
            case IOSuccess(value):
                return IOSuccess([UserRead.model_validate(u) for u in value.unwrap()])
            case IOFailure(value):
                return IOFailure(NoItemsFoundError(query=value.failure().args[0]))
            case _:
                return IOFailure(
                    NoItemsFoundError(
                        query="Unknown Error occurred while getting all users",
                    )
                )

    async def get_user_by_id(
        self, user_id: UUID
    ) -> IOResult[UserRead, UserNotFoundError]:
        result = await self.user_repository.get_by_id(user_id)
        match result:
            case IOSuccess(value):
                return IOSuccess(UserRead.model_validate(value.unwrap()))
            case IOFailure(value):
                return IOFailure(
                    UserNotFoundError(
                        identifier=str(user_id), message=str(value.failure().args[0])
                    )
                )
            case _:
                return IOFailure(UserNotFoundError(identifier=str(user_id)))

    async def get_user_by_email(
        self, email: str
    ) -> IOResult[UserRead, UserNotFoundError]:
        result = await self.user_repository.get_by_email(email)
        match result:
            case IOSuccess(value):
                return IOSuccess(UserRead.model_validate(value.unwrap()))
            case IOFailure(value):
                return IOFailure(
                    UserNotFoundError(
                        identifier=email, message=str(value.failure().args[0])
                    )
                )
            case _:
                return IOFailure(UserNotFoundError(identifier=email))
