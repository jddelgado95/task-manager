from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_returns_404():
    response = client.get("/")
    assert response.status_code == 404  # adjust based on your route behavior