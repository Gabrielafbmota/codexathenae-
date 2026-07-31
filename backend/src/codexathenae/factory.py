"""Application factory: creates and configures the FastAPI instance."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient

from codexathenae.infrastructure.observability.logging import configure_logging, get_logger
from codexathenae.infrastructure.persistence.mongodb.indexes import ensure_indexes
from codexathenae.infrastructure.settings.config import Settings
from codexathenae.presentation.api.exception_handlers import register_exception_handlers
from codexathenae.presentation.api.routers import books_router, health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        from codexathenae.infrastructure.settings.config import get_settings

        settings = get_settings()

    configure_logging(log_level=settings.log_level, debug=settings.debug)
    logger = get_logger(__name__)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info("Starting up CodexAthenae", version=settings.app_version)

        client: AsyncMongoClient[dict[str, object]] = AsyncMongoClient(settings.mongodb_uri)
        app.state.mongo_client = client
        app.state.mongo_db_name = settings.mongodb_database

        await ensure_indexes(client, settings.mongodb_database)
        logger.info("MongoDB connected", database=settings.mongodb_database)

        yield

        logger.info("Shutting down — closing MongoDB connection")
        await client.aclose()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(books_router)

    return app
