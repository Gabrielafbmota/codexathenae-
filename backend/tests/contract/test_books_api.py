"""Contract tests for the books API endpoints."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from codexathenae.application.dto.book_dto import (
    BookDTO,
    BookListDTO,
    PublicationMetadataDTO,
    ReadingProgressDTO,
)
from codexathenae.application.ports.book_repository import BookRepository
from codexathenae.domain.enums.reading_status import ReadingStatus
from codexathenae.domain.exceptions.book_exceptions import BookNotFoundError, DuplicateISBNError


def _now() -> Any:
    from datetime import UTC, datetime

    return datetime.now(UTC)


def _make_dto(
    id: str = "00000000-0000-0000-0000-000000000001",
    title: str = "Clean Code",
    isbn_13: str | None = None,
) -> BookDTO:
    return BookDTO(
        id=id,
        title=title,
        authors=["Robert Martin"],
        isbn_10=None,
        isbn_13=isbn_13,
        status=ReadingStatus.WANT_TO_READ,
        publication=PublicationMetadataDTO(),
        cover_url=None,
        progress=ReadingProgressDTO(),
        created_at=_now(),
        updated_at=_now(),
    )


class TestCreateBook:
    @pytest.mark.anyio
    async def test_create_book_returns_201(
        self,
        client: AsyncClient,
        app_with_mock_repo: tuple[Any, BookRepository],
    ) -> None:
        _, repo = app_with_mock_repo
        dto = _make_dto(title="Clean Code")
        repo.get_by_isbn = AsyncMock(return_value=None)
        repo.create = AsyncMock()

        from codexathenae.application.use_cases import create_book as uc_module

        original_execute = uc_module.CreateBookUseCase.execute

        async def fake_execute(self: Any, command: Any) -> BookDTO:
            return dto

        uc_module.CreateBookUseCase.execute = fake_execute  # type: ignore[method-assign]
        try:
            response = await client.post(
                "/api/v1/books",
                json={"title": "Clean Code", "authors": ["Robert Martin"]},
            )
            assert response.status_code == 201
            body = response.json()
            assert body["title"] == "Clean Code"
            assert "Location" in response.headers
            assert body["id"] == dto.id
        finally:
            uc_module.CreateBookUseCase.execute = original_execute  # type: ignore[method-assign]

    @pytest.mark.anyio
    async def test_create_book_missing_title_returns_422(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/v1/books",
            json={"authors": ["Robert Martin"]},
        )
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_create_book_empty_authors_returns_422(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/v1/books",
            json={"title": "Clean Code", "authors": []},
        )
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_create_book_duplicate_isbn_returns_409(
        self,
        client: AsyncClient,
    ) -> None:
        from codexathenae.application.use_cases import create_book as uc_module

        original_execute = uc_module.CreateBookUseCase.execute

        async def raise_dup(self: Any, command: Any) -> BookDTO:
            raise DuplicateISBNError("9780306406157")

        uc_module.CreateBookUseCase.execute = raise_dup  # type: ignore[method-assign]
        try:
            response = await client.post(
                "/api/v1/books",
                json={"title": "Clean Code", "authors": ["Author"], "isbn": "9780306406157"},
            )
            assert response.status_code == 409
            body = response.json()
            assert body["code"] == "DUPLICATE_ISBN"
        finally:
            uc_module.CreateBookUseCase.execute = original_execute  # type: ignore[method-assign]

    @pytest.mark.anyio
    async def test_internal_fields_not_exposed(
        self,
        client: AsyncClient,
    ) -> None:
        dto = _make_dto()
        from codexathenae.application.use_cases import create_book as uc_module

        original_execute = uc_module.CreateBookUseCase.execute

        async def fake_execute(self: Any, command: Any) -> BookDTO:
            return dto

        uc_module.CreateBookUseCase.execute = fake_execute  # type: ignore[method-assign]
        try:
            response = await client.post(
                "/api/v1/books",
                json={"title": "Clean Code", "authors": ["Robert Martin"]},
            )
            body = response.json()
            assert "deleted_at" not in body
            assert "enrichment" not in body
        finally:
            uc_module.CreateBookUseCase.execute = original_execute  # type: ignore[method-assign]


class TestGetBook:
    @pytest.mark.anyio
    async def test_get_nonexistent_book_returns_404(
        self,
        client: AsyncClient,
    ) -> None:
        from codexathenae.application.use_cases import get_book as uc_module

        original_execute = uc_module.GetBookUseCase.execute

        async def raise_not_found(self: Any, book_id: str) -> BookDTO:
            raise BookNotFoundError(book_id)

        uc_module.GetBookUseCase.execute = raise_not_found  # type: ignore[method-assign]
        try:
            response = await client.get("/api/v1/books/00000000-0000-0000-0000-000000000099")
            assert response.status_code == 404
            body = response.json()
            assert body["code"] == "BOOK_NOT_FOUND"
        finally:
            uc_module.GetBookUseCase.execute = original_execute  # type: ignore[method-assign]


class TestListBooks:
    @pytest.mark.anyio
    async def test_list_books_returns_200(
        self,
        client: AsyncClient,
    ) -> None:
        dto = _make_dto()
        from codexathenae.application.dto.book_dto import BookListDTO
        from codexathenae.application.use_cases import list_books as uc_module

        original_execute = uc_module.ListBooksUseCase.execute

        async def fake_execute(self: Any, filters: Any) -> BookListDTO:
            return BookListDTO(items=[dto], total=1, limit=20, offset=0)

        uc_module.ListBooksUseCase.execute = fake_execute  # type: ignore[method-assign]
        try:
            response = await client.get("/api/v1/books")
            assert response.status_code == 200
            body = response.json()
            assert body["total"] == 1
            assert len(body["items"]) == 1
        finally:
            uc_module.ListBooksUseCase.execute = original_execute  # type: ignore[method-assign]
