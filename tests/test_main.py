from datetime import timezone

import pytest
from httpx import AsyncClient

from app import app
from app.db.migrations.initial_currencies import last_update_time


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_read_last_update_time(client: AsyncClient):
    response = await client.get("/last-update-time")
    assert response.status_code == 200
    expected_time = last_update_time.astimezone(timezone.utc).isoformat()
    assert response.json() == {"last_update_time": expected_time}
