"""
Abstract port for book persistence.

Lives in the application layer; must not import from infrastructure.
Callers depend on this interface, never on a concrete implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from codexathenae.application.dto.book_dto import BookListDTO, BookQueryFilters
from codexathenae.domain.entities.book import Book
from codexathenae.domain.value_objects.book_id import BookId
from codexathenae.domain.value_objects.isbn import ISBN


class BookRepository(ABC):
    @abstractmethod
    async def create(self, book: Book) -> None:
        """
        Persist a new book.

        Raises DuplicateISBNError if a non-deleted book with the same ISBN
        already exists.
        """

    @abstractmethod
    async def get_by_id(self, book_id: BookId) -> Book | None:
        """
        Return the book with the given ID, or None if not found.

        Soft-deleted books are NOT returned.
        """

    @abstractmethod
    async def get_by_isbn(self, isbn: ISBN) -> Book | None:
        """
        Return the first non-deleted book matching the given ISBN, or None.

        The match must consider both ISBN-10 and ISBN-13 slots.
        """

    @abstractmethod
    async def list(self, filters: BookQueryFilters) -> BookListDTO:
        """
        Return a paginated list of books matching the given filters.

        Soft-deleted books are excluded unless filters.include_deleted is True.
        The returned BookListDTO includes the total count before pagination.
        """

    @abstractmethod
    async def update(self, book: Book) -> None:
        """
        Persist all changes to an existing book.

        Raises BookNotFoundError if no document with book.id exists.
        """

    @abstractmethod
    async def soft_delete(self, book_id: BookId) -> None:
        """
        Mark the book as deleted without removing it from the collection.

        Raises BookNotFoundError if the book does not exist.
        Has no effect if the book is already soft-deleted.
        """
