from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_db_connection():
    response = client.get("/health-db")
    assert response.status_code == 200
    assert response.json() == {"status": "connected"}
