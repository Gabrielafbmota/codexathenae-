"""FastAPI dependency providers for use cases."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import Depends, Request

from codexathenae.application.use_cases import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookUseCase,
    ListBooksUseCase,
    UpdateBookUseCase,
)
from codexathenae.infrastructure.persistence.mongodb.repository import MongoBookRepository


def _get_repository(request: Request) -> MongoBookRepository:
    client: Any = request.app.state.mongo_client
    db_name: str = request.app.state.mongo_db_name
    return MongoBookRepository(client, db_name)


def get_create_book_use_case(
    repo: Annotated[MongoBookRepository, Depends(_get_repository)],
) -> CreateBookUseCase:
    return CreateBookUseCase(repo)


def get_get_book_use_case(
    repo: Annotated[MongoBookRepository, Depends(_get_repository)],
) -> GetBookUseCase:
    return GetBookUseCase(repo)


def get_list_books_use_case(
    repo: Annotated[MongoBookRepository, Depends(_get_repository)],
) -> ListBooksUseCase:
    return ListBooksUseCase(repo)


def get_update_book_use_case(
    repo: Annotated[MongoBookRepository, Depends(_get_repository)],
) -> UpdateBookUseCase:
    return UpdateBookUseCase(repo)


def get_delete_book_use_case(
    repo: Annotated[MongoBookRepository, Depends(_get_repository)],
) -> DeleteBookUseCase:
    return DeleteBookUseCase(repo)
