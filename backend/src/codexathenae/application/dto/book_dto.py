from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from codexathenae.domain.enums.reading_status import ReadingStatus


@dataclass(frozen=True)
class CreateBookCommand:
    title: str
    authors: list[str]
    isbn: str | None = None
    status: ReadingStatus = ReadingStatus.WANT_TO_READ
    publisher: str | None = None
    published_year: int | None = None
    page_count: int | None = None
    language: str | None = None
    description: str | None = None
    cover_url: str | None = None


@dataclass(frozen=True)
class UpdateBookCommand:
    book_id: str
    title: str | None = None
    authors: list[str] | None = None
    publisher: str | None = None
    published_year: int | None = None
    page_count: int | None = None
    language: str | None = None
    description: str | None = None
    cover_url: str | None = None


@dataclass(frozen=True)
class BookQueryFilters:
    status: ReadingStatus | None = None
    include_deleted: bool = False
    limit: int = 20
    offset: int = 0


@dataclass(frozen=True)
class PublicationMetadataDTO:
    publisher: str | None = None
    published_year: int | None = None
    original_year: int | None = None
    language: str | None = None
    page_count: int | None = None
    genres: list[str] = field(default_factory=list)
    description: str | None = None
    subtitle: str | None = None


@dataclass(frozen=True)
class ReadingProgressDTO:
    pages_read: int = 0
    total_pages: int | None = None
    percentage: float | None = None


@dataclass(frozen=True)
class BookDTO:
    id: str
    title: str
    authors: list[str]
    isbn_10: str | None
    isbn_13: str | None
    status: ReadingStatus
    publication: PublicationMetadataDTO
    cover_url: str | None
    progress: ReadingProgressDTO
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    rating: float | None = None
    notes: str | None = None


@dataclass(frozen=True)
class BookListDTO:
    items: list[BookDTO]
    total: int
    limit: int
    offset: int
