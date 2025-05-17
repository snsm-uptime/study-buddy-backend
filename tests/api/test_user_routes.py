# tests/api/test_user_routes.py

import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient
from returns.io import IOFailure, IOSuccess

from app.errors import FormValidationError, NoItemsFoundError
from app.main import app
from app.schemas.user import UserCreate, UserRead


@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient, mock_user_service: AsyncMock):
    # Arrange
    user_data = UserCreate(email="seb@example.com", name="Seb", password="secure123")
    fake_user = UserRead(
        id=uuid.uuid4(),
        email=user_data.email,
        name=user_data.name,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
    )

    mock_user_service.create_user.return_value = IOSuccess(fake_user)

    response = await client.post("/users/", json=user_data.model_dump())

    assert response.status_code == 201
    assert response.json()["email"] == user_data.email


@pytest.mark.asyncio
async def test_create_user_already_exists(
    client: AsyncClient, mock_user_service: AsyncMock
):
    # Arrange
    user_data = UserCreate(email="seb@example.com", name="Seb", password="secure123")

    # Simulate service returning a failure (already exists)
    error = FormValidationError(field="email", message="Email already registered")
    mock_user_service.create_user.return_value = IOFailure(error)

    # Act
    response = await client.post("/users/", json=user_data.model_dump())

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_users_success(client: AsyncClient, mock_user_service: AsyncMock):
    fake_users = [
        UserRead(
            id=uuid.uuid4(),
            email="a@example.com",
            name="Alice",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        ),
        UserRead(
            id=uuid.uuid4(),
            email="b@example.com",
            name="Bob",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        ),
    ]
    mock_user_service.get_users.return_value = IOSuccess(fake_users)

    response = await client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[0]["email"] == "a@example.com"


@pytest.mark.asyncio
async def test_get_users_failure(client: AsyncClient, mock_user_service: AsyncMock):
    mock_user_service.get_users.return_value = IOFailure(NoItemsFoundError("all users"))

    response = await client.get("/users/")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_get_user_by_id_success(
    client: AsyncClient, mock_user_service: AsyncMock
):
    user_id = uuid.uuid4()
    fake_user = UserRead(
        id=user_id,
        email="id@example.com",
        name="IdName",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
    )

    mock_user_service.get_user_by_id.return_value = IOSuccess(fake_user)

    response = await client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "id@example.com"
