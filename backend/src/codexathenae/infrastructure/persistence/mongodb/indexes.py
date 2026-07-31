"""Create MongoDB indexes idempotently at startup."""

from __future__ import annotations

from typing import Any

from pymongo import ASCENDING, AsyncMongoClient


async def ensure_indexes(client: AsyncMongoClient[dict[str, Any]], database_name: str) -> None:
    col = client[database_name]["books"]

    # Unique partial index on isbn_13 (only for non-null, non-deleted documents)
    await col.create_index(
        [("isbn_13", ASCENDING)],
        unique=True,
        partialFilterExpression={"isbn_13": {"$type": "string"}, "deleted_at": None},
        name="unique_isbn_13_active",
        background=True,
    )

    # Unique partial index on isbn_10 (only for non-null, non-deleted documents)
    await col.create_index(
        [("isbn_10", ASCENDING)],
        unique=True,
        partialFilterExpression={"isbn_10": {"$type": "string"}, "deleted_at": None},
        name="unique_isbn_10_active",
        background=True,
    )

    # Status + created_at for filtered listing queries
    await col.create_index(
        [("status", ASCENDING), ("created_at", ASCENDING)],
        name="status_created_at",
        background=True,
    )

    # Soft-delete filter
    await col.create_index(
        [("deleted_at", ASCENDING)],
        name="deleted_at",
        background=True,
    )
