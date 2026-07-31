from __future__ import annotations

from typing import Any

from pymongo import AsyncMongoClient
from pymongo.errors import DuplicateKeyError

from codexathenae.application.dto.book_dto import BookDTO, BookListDTO, BookQueryFilters
from codexathenae.application.ports.book_repository import BookRepository
from codexathenae.application.use_cases._mapper import book_to_dto
from codexathenae.domain.entities.book import Book
from codexathenae.domain.exceptions.book_exceptions import BookNotFoundError, DuplicateISBNError
from codexathenae.domain.value_objects.book_id import BookId
from codexathenae.domain.value_objects.isbn import ISBN
from codexathenae.infrastructure.persistence.mongodb.mapper import (
    book_to_document,
    document_to_book,
)

_COLLECTION = "books"


class MongoBookRepository(BookRepository):
    def __init__(self, client: AsyncMongoClient[dict[str, Any]], database_name: str) -> None:
        self._db = client[database_name]
        self._col = self._db[_COLLECTION]

    async def create(self, book: Book) -> None:
        doc = book_to_document(book)
        try:
            await self._col.insert_one(doc)
        except DuplicateKeyError as exc:
            isbn = book.isbn_13 or book.isbn_10
            if isbn:
                raise DuplicateISBNError(isbn.value) from exc
            raise

    async def get_by_id(self, book_id: BookId) -> Book | None:
        doc = await self._col.find_one({"_id": book_id.value, "deleted_at": None})
        if doc is None:
            return None
        return document_to_book(doc)

    async def get_by_isbn(self, isbn: ISBN) -> Book | None:
        field = "isbn_13" if isbn.is_isbn13 else "isbn_10"
        doc = await self._col.find_one({field: isbn.value, "deleted_at": None})
        if doc is None:
            return None
        return document_to_book(doc)

    async def list(self, filters: BookQueryFilters) -> BookListDTO:
        query: dict[str, Any] = {}
        if not filters.include_deleted:
            query["deleted_at"] = None
        if filters.status is not None:
            query["status"] = filters.status.value

        total = await self._col.count_documents(query)
        cursor = (
            self._col.find(query).sort("created_at", -1).skip(filters.offset).limit(filters.limit)
        )
        docs = await cursor.to_list(length=filters.limit)
        books = [document_to_book(d) for d in docs]
        items: list[BookDTO] = [book_to_dto(b) for b in books]
        return BookListDTO(
            items=items,
            total=total,
            limit=filters.limit,
            offset=filters.offset,
        )

    async def update(self, book: Book) -> None:
        doc = book_to_document(book)
        doc.pop("_id", None)
        result = await self._col.update_one({"_id": book.id.value}, {"$set": doc})
        if result.matched_count == 0:
            raise BookNotFoundError(book.id.value)

    async def soft_delete(self, book_id: BookId) -> None:
        from datetime import UTC, datetime

        result = await self._col.update_one(
            {"_id": book_id.value, "deleted_at": None},
            {"$set": {"deleted_at": datetime.now(UTC), "updated_at": datetime.now(UTC)}},
        )
        if result.matched_count == 0:
            existing = await self._col.find_one({"_id": book_id.value})
            if existing is None:
                raise BookNotFoundError(book_id.value)
