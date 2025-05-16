import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService


@pytest.mark.asyncio
# @pytest.mark.skip("Not implemented yet")
async def test_create_user(
    client: AsyncClient,
    db_session: AsyncSession,
):
    # Arrange
    user_data = UserCreate(
        email="seb@example.com",
        name="Seb",
        password="testpassword123",
    )

    # Make sure it doesn't already exist
    user_repo = UserRepository(db_session)
    user_service = UserService(user_repo)
    try:
        existing = await user_service.get_user_by_email(user_data.email)
        assert existing is None
    except Exception as e:
        # If the user doesn't exist, we can proceed
        assert str(e) == "User not found"

    # Act
    response = await client.post(
        "/users/", json=user_data.model_dump(), follow_redirects=False
    )

    # Assert
    assert (
        response.status_code != 307
    ), f"Redirected to {response.headers.get('location')}"
    data = response.json()

    assert data["email"] == user_data.email
    assert data["name"] == user_data.name
    assert "id" in data and uuid.UUID(data["id"])  # valid UUID
    assert "created_at" in data
