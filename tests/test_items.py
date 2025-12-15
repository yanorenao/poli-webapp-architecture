import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/items/", json={"title": "Test Item", "description": "A test"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Item"

@pytest.mark.asyncio
async def test_read_items():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)