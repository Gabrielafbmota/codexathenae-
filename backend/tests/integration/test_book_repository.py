"""Integration tests for MongoBookRepository against a real MongoDB instance."""

from __future__ import annotations

import pytest

from codexathenae.application.dto.book_dto import BookQueryFilters
from codexathenae.domain.entities.book import Book
from codexathenae.domain.enums.reading_status import ReadingStatus
from codexathenae.domain.exceptions.book_exceptions import BookNotFoundError, DuplicateISBNError
from codexathenae.domain.value_objects.isbn import ISBN
from codexathenae.infrastructure.persistence.mongodb.repository import MongoBookRepository


def _book(title: str = "Test Book", isbn: str | None = None) -> Book:
    isbn_13 = ISBN(isbn) if isbn and len(isbn) == 13 else None
    isbn_10 = ISBN(isbn) if isbn and len(isbn) == 10 else None
    return Book.create(title=title, authors=["Author"], isbn_13=isbn_13, isbn_10=isbn_10)


class TestCreate:
    @pytest.mark.anyio
    async def test_create_and_retrieve(self, repo: MongoBookRepository) -> None:
        book = _book("Clean Code")
        await repo.create(book)
        found = await repo.get_by_id(book.id)
        assert found is not None
        assert found.title == "Clean Code"

    @pytest.mark.anyio
    async def test_duplicate_isbn13_raises(self, repo: MongoBookRepository) -> None:
        isbn = "9780306406157"
        await repo.create(_book(isbn=isbn))
        with pytest.raises(DuplicateISBNError):
            await repo.create(_book("Another", isbn=isbn))

    @pytest.mark.anyio
    async def test_two_books_without_isbn_allowed(self, repo: MongoBookRepository) -> None:
        await repo.create(_book("Book A"))
        await repo.create(_book("Book B"))
        result = await repo.list(BookQueryFilters())
        assert result.total == 2


class TestGetByIsbn:
    @pytest.mark.anyio
    async def test_get_by_isbn13(self, repo: MongoBookRepository) -> None:
        isbn = "9780306406157"
        book = _book(isbn=isbn)
        await repo.create(book)
        found = await repo.get_by_isbn(ISBN(isbn))
        assert found is not None
        assert found.id == book.id

    @pytest.mark.anyio
    async def test_get_by_isbn_not_found(self, repo: MongoBookRepository) -> None:
        result = await repo.get_by_isbn(ISBN("9780306406157"))
        assert result is None


class TestList:
    @pytest.mark.anyio
    async def test_list_returns_books(self, repo: MongoBookRepository) -> None:
        await repo.create(_book("A"))
        await repo.create(_book("B"))
        result = await repo.list(BookQueryFilters(limit=10))
        assert result.total == 2
        assert len(result.items) == 2

    @pytest.mark.anyio
    async def test_list_filters_by_status(self, repo: MongoBookRepository) -> None:
        book = _book("Reading Book")
        await repo.create(book)
        reading_filters = BookQueryFilters(status=ReadingStatus.READING)
        result = await repo.list(reading_filters)
        assert result.total == 0

    @pytest.mark.anyio
    async def test_list_excludes_deleted(self, repo: MongoBookRepository) -> None:
        book = _book("Will be deleted")
        await repo.create(book)
        await repo.soft_delete(book.id)
        result = await repo.list(BookQueryFilters())
        assert result.total == 0

    @pytest.mark.anyio
    async def test_pagination(self, repo: MongoBookRepository) -> None:
        for i in range(5):
            await repo.create(_book(f"Book {i}"))
        page1 = await repo.list(BookQueryFilters(limit=3, offset=0))
        page2 = await repo.list(BookQueryFilters(limit=3, offset=3))
        assert len(page1.items) == 3
        assert len(page2.items) == 2
        assert page1.total == 5


class TestUpdate:
    @pytest.mark.anyio
    async def test_update_book(self, repo: MongoBookRepository) -> None:
        book = _book("Old Title")
        await repo.create(book)
        book.update_metadata(title="New Title")
        await repo.update(book)
        found = await repo.get_by_id(book.id)
        assert found is not None
        assert found.title == "New Title"

    @pytest.mark.anyio
    async def test_update_nonexistent_raises(self, repo: MongoBookRepository) -> None:
        book = _book("Ghost")
        with pytest.raises(BookNotFoundError):
            await repo.update(book)


class TestSoftDelete:
    @pytest.mark.anyio
    async def test_soft_delete_hides_book(self, repo: MongoBookRepository) -> None:
        book = _book("Will Be Deleted")
        await repo.create(book)
        await repo.soft_delete(book.id)
        found = await repo.get_by_id(book.id)
        assert found is None

    @pytest.mark.anyio
    async def test_soft_delete_nonexistent_raises(self, repo: MongoBookRepository) -> None:
        book = _book("Ghost")
        with pytest.raises(BookNotFoundError):
            await repo.soft_delete(book.id)

    @pytest.mark.anyio
    async def test_isbn_reusable_after_soft_delete(self, repo: MongoBookRepository) -> None:
        isbn = "9780306406157"
        book = _book(isbn=isbn)
        await repo.create(book)
        await repo.soft_delete(book.id)
        # A new book with the same ISBN should now be allowed
        new_book = _book("New Book Same ISBN", isbn=isbn)
        await repo.create(new_book)
        found = await repo.get_by_isbn(ISBN(isbn))
        assert found is not None
        assert found.id == new_book.id
