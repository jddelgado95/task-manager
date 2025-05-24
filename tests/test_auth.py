#Example for /register
#This test checks if a user can register successfully.

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user(client):
    response = client.post("/register", json={
        "username": "testuser_3",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser_3"
    assert "id" in data