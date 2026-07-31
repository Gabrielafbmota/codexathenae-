"""Contract tests for health endpoints."""

import pytest
from httpx import AsyncClient


class TestHealthLive:
    @pytest.mark.anyio
    async def test_live_returns_200(self, client: AsyncClient) -> None:
        response = await client.get("/health/live")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestHealthReady:
    @pytest.mark.anyio
    async def test_ready_returns_200_when_mongo_ok(self, client: AsyncClient) -> None:
        response = await client.get("/health/ready")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["checks"]["mongodb"] == "ok"
