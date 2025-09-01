import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.fastapi_mcp_demo.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
@pytest.mark.asyncio
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac