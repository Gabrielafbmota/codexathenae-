"""Unit tests for CreateBookUseCase."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from codexathenae.application.dto.book_dto import (
    BookDTO,
    CreateBookCommand,
)
from codexathenae.application.ports.book_repository import BookRepository
from codexathenae.application.use_cases.create_book import CreateBookUseCase
from codexathenae.domain.enums.reading_status import ReadingStatus
from codexathenae.domain.exceptions.book_exceptions import DuplicateISBNError, InvalidISBNError


def _make_repo(*, existing_isbn: bool = False) -> BookRepository:
    repo = MagicMock(spec=BookRepository)
    repo.create = AsyncMock()
    repo.get_by_isbn = AsyncMock(return_value=MagicMock() if existing_isbn else None)
    return repo


class TestCreateBookUseCase:
    @pytest.mark.anyio
    async def test_creates_book_without_isbn(self) -> None:
        repo = _make_repo()
        use_case = CreateBookUseCase(repo)
        cmd = CreateBookCommand(title="Clean Code", authors=["Robert Martin"])
        dto = await use_case.execute(cmd)

        assert dto.title == "Clean Code"
        assert dto.authors == ["Robert Martin"]
        assert dto.isbn_10 is None
        assert dto.isbn_13 is None
        assert dto.status == ReadingStatus.WANT_TO_READ
        repo.create.assert_awaited_once()

    @pytest.mark.anyio
    async def test_creates_book_with_isbn13(self) -> None:
        repo = _make_repo()
        use_case = CreateBookUseCase(repo)
        cmd = CreateBookCommand(title="Clean Code", authors=["Robert Martin"], isbn="9780306406157")
        dto = await use_case.execute(cmd)
        assert dto.isbn_13 == "9780306406157"

    @pytest.mark.anyio
    async def test_creates_book_with_isbn10(self) -> None:
        repo = _make_repo()
        use_case = CreateBookUseCase(repo)
        cmd = CreateBookCommand(title="Clean Code", authors=["Robert Martin"], isbn="0306406152")
        dto = await use_case.execute(cmd)
        assert dto.isbn_10 == "0306406152"

    @pytest.mark.anyio
    async def test_raises_on_invalid_isbn(self) -> None:
        repo = _make_repo()
        use_case = CreateBookUseCase(repo)
        # 0000000001 has checksum 1, not divisible by 11 → invalid
        cmd = CreateBookCommand(title="Clean Code", authors=["Robert Martin"], isbn="0000000001")
        with pytest.raises(InvalidISBNError):
            await use_case.execute(cmd)
        repo.create.assert_not_awaited()

    @pytest.mark.anyio
    async def test_raises_on_duplicate_isbn(self) -> None:
        repo = _make_repo(existing_isbn=True)
        use_case = CreateBookUseCase(repo)
        cmd = CreateBookCommand(title="Clean Code", authors=["Robert Martin"], isbn="9780306406157")
        with pytest.raises(DuplicateISBNError):
            await use_case.execute(cmd)
        repo.create.assert_not_awaited()

    @pytest.mark.anyio
    async def test_isbn_is_normalized(self) -> None:
        repo = _make_repo()
        use_case = CreateBookUseCase(repo)
        cmd = CreateBookCommand(title="Clean Code", authors=["Author"], isbn="978-0-306-40615-7")
        dto = await use_case.execute(cmd)
        assert dto.isbn_13 == "9780306406157"

    @pytest.mark.anyio
    async def test_returns_dto_not_domain_entity(self) -> None:
        repo = _make_repo()
        use_case = CreateBookUseCase(repo)
        cmd = CreateBookCommand(title="Test", authors=["Author"])
        result = await use_case.execute(cmd)
        assert isinstance(result, BookDTO)
