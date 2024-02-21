import asyncio
from datetime import timezone

import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app import app
from app.db.migrations.initial_currencies import last_update_time


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_read_last_update_time(client: AsyncClient):
    # Get last response time
    response = await client.get("/last-update-time")
    assert response.status_code == 200

    # Assert it is the same as initial last update time
    expected_time = last_update_time.astimezone(timezone.utc).strftime("%d-%b-%Y %H:%M")
    assert response.json() == {"last_update_time": expected_time}


@pytest.mark.asyncio
async def test_convert_endpoint_success(client: AsyncClient, mocker: MockerFixture):
    # Mock convert_currency
    mocker.patch(
        "app.main.convert_currency",
        return_value=50
    )

    # Send a currency conversion request
    response = await client.get("/convert?source=EUR&target=USD&amount=100")

    # Check the successful response and correctness of the conversion result
    assert response.status_code == 200
    assert response.json() == {"converted_amount": 50}


@pytest.mark.asyncio
async def test_convert_bad_currency(client: AsyncClient):
    # UNKNOWN is bad currency name
    response = await client.get("/convert?source=UNKNOWN&target=USD&amount=100")  # Use "UNKNOWN" as the source
    assert response.status_code == 400
    assert response.json() == {"detail": "Currency UNKNOWN is not available."}

