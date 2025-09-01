import pytest
from fastapi.testclient import TestClient
from src.fastapi_mcp_demo.main import app

def test_hello_world(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_health_check(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "mcp_status" in data

def test_list_mcp_functions(client: TestClient):
    response = client.get("/api/v1/mcp/functions")
    assert response.status_code == 200
    data = response.json()
    assert "functions" in data
    assert len(data["functions"]) > 0