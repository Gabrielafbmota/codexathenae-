"""
Contract test fixtures.

The FastAPI lifespan is intercepted so that tests never need a real MongoDB.
Patches must remain active through the lifespan startup/shutdown, so they
wrap the AsyncClient context manager.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from codexathenae.application.dto.book_dto import BookListDTO
from codexathenae.application.ports.book_repository import BookRepository
from codexathenae.factory import create_app
from codexathenae.infrastructure.settings.config import Settings


def _make_mock_repo() -> BookRepository:
    repo = MagicMock(spec=BookRepository)
    repo.create = AsyncMock()
    repo.get_by_isbn = AsyncMock(return_value=None)
    repo.get_by_id = AsyncMock(return_value=None)
    repo.update = AsyncMock()
    repo.soft_delete = AsyncMock()
    repo.list = AsyncMock(return_value=BookListDTO(items=[], total=0, limit=20, offset=0))
    return repo


def _make_fake_mongo_client() -> Any:
    client = MagicMock()
    client.admin.command = AsyncMock()
    # Make getitem return a MagicMock so client[db][collection] works
    client.__getitem__ = MagicMock(return_value=MagicMock())
    client.close = MagicMock()
    return client


@pytest.fixture()
def settings() -> Settings:
    return Settings(
        MONGODB_URI="mongodb://localhost:27017",
        MONGODB_DATABASE="codexathenae_test",
    )


@pytest.fixture()
async def app_and_repo(
    settings: Settings,
) -> AsyncGenerator[tuple[FastAPI, BookRepository, AsyncClient], None]:
    mock_repo = _make_mock_repo()
    fake_client = _make_fake_mongo_client()

    # Patches must wrap AsyncClient so they are active during lifespan startup
    with (
        patch("codexathenae.factory.AsyncMongoClient", return_value=fake_client),
        patch("codexathenae.factory.ensure_indexes", new=AsyncMock()),
    ):
        _app = create_app(settings)

        # Override the repository dependency so use cases get mock_repo
        from codexathenae.presentation.api.dependencies.use_cases import _get_repository

        _app.dependency_overrides[_get_repository] = lambda: mock_repo

        # ASGITransport does NOT invoke the ASGI lifespan, so we set state manually
        _app.state.mongo_client = fake_client
        _app.state.mongo_db_name = settings.mongodb_database

        async with AsyncClient(transport=ASGITransport(app=_app), base_url="http://test") as ac:
            yield _app, mock_repo, ac

        _app.dependency_overrides.clear()


@pytest.fixture()
async def client(
    app_and_repo: tuple[FastAPI, BookRepository, AsyncClient],
) -> AsyncClient:
    _, _, ac = app_and_repo
    return ac


@pytest.fixture()
async def app_with_mock_repo(
    app_and_repo: tuple[FastAPI, BookRepository, AsyncClient],
) -> tuple[FastAPI, BookRepository]:
    _app, repo, _ = app_and_repo
    return _app, repo
