import io
from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import mark

from app.main import app

client = TestClient(app)


@mark.skip("Not implemented yet")
def test_upload_file_returns_file_metadata():
    file_content = b"This is a test document."
    file_name = "test.txt"
    response = client.post(
        "/files/upload",
        files={"file": (file_name, io.BytesIO(file_content), "text/plain")},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["title"] == file_name
    assert "id" in data
    assert "size_kb" in data
    assert data["size_kb"] > 0
