"""
Integration test fixtures using a real MongoDB instance.

In CI, set MONGODB_URI to point to the service container.
Locally, the default connects to mongodb://localhost:27017.

AsyncMongoClient binds to its event loop; fixtures are function-scoped so each
test shares the same loop as its client.
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from typing import Any

import pytest

from codexathenae.infrastructure.persistence.mongodb.indexes import ensure_indexes
from codexathenae.infrastructure.persistence.mongodb.repository import MongoBookRepository

_TEST_DB = "test_codexathenae"
_DEFAULT_URI = "mongodb://localhost:27017"


@pytest.fixture()
async def mongo_client() -> AsyncGenerator[Any, None]:
    from pymongo import AsyncMongoClient

    uri = os.environ.get("MONGODB_URI", _DEFAULT_URI)
    client: AsyncMongoClient[dict[str, Any]] = AsyncMongoClient(uri)
    await ensure_indexes(client, _TEST_DB)
    yield client
    await client.aclose()


@pytest.fixture()
async def repo(mongo_client: Any) -> AsyncGenerator[MongoBookRepository, None]:
    repository = MongoBookRepository(mongo_client, _TEST_DB)
    yield repository
    await mongo_client[_TEST_DB]["books"].delete_many({})
