from fastapi.testclient import TestClient
from pytest import mark

from app.main import app

client = TestClient(app)


@mark.skip("Not Implemented")
def test_summary_returns_summary_text():
    response = client.post("/prompt/summary", json={"text": "This is a long document."})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)
