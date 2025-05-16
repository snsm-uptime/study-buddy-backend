import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService


@pytest.mark.asyncio
@pytest.mark.skip("Not implemented yet")
async def test_get_user_by_id(client: AsyncClient, db_session: AsyncSession):
    # Arrange: create a user
    repo = UserRepository(db_session)
    service = UserService(repo)
    created = await service.create_user(
        UserCreate(email="getme@example.com", name="Get Me", password="secret123")
    )

    # Act
    response = await client.get(f"/users/{created.id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(created.id)
    assert data["email"] == created.email
    assert data["name"] == created.name


@pytest.mark.asyncio
@pytest.mark.skip("Not implemented yet")
async def test_get_user_404(client: AsyncClient):
    # Act
    response = await client.get(f"/users/{uuid.uuid4()}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
