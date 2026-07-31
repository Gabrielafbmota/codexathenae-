from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from codexathenae.domain.enums.reading_status import ReadingStatus


class BookCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    authors: list[str] = Field(..., min_length=1)
    isbn: str | None = Field(default=None, max_length=20)
    status: ReadingStatus = ReadingStatus.WANT_TO_READ
    publisher: str | None = Field(default=None, max_length=200)
    published_year: int | None = Field(default=None, ge=1, le=2100)
    page_count: int | None = Field(default=None, ge=1)
    language: str | None = Field(default=None, max_length=10)
    description: str | None = Field(default=None, max_length=5000)
    cover_url: str | None = Field(default=None, max_length=2048)

    @field_validator("authors")
    @classmethod
    def authors_not_empty_strings(cls, v: list[str]) -> list[str]:
        stripped = [a.strip() for a in v if a.strip()]
        if not stripped:
            raise ValueError("authors must contain at least one non-empty name")
        return stripped

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title cannot be blank")
        return v


class BookUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    authors: list[str] | None = None
    publisher: str | None = Field(default=None, max_length=200)
    published_year: int | None = Field(default=None, ge=1, le=2100)
    page_count: int | None = Field(default=None, ge=1)
    language: str | None = Field(default=None, max_length=10)
    description: str | None = Field(default=None, max_length=5000)
    cover_url: str | None = Field(default=None, max_length=2048)


class PublicationMetadataResponse(BaseModel):
    publisher: str | None = None
    published_year: int | None = None
    original_year: int | None = None
    language: str | None = None
    page_count: int | None = None
    genres: list[str] = Field(default_factory=list)
    description: str | None = None
    subtitle: str | None = None


class ReadingProgressResponse(BaseModel):
    pages_read: int = 0
    total_pages: int | None = None
    percentage: float | None = None


class BookResponse(BaseModel):
    id: str
    title: str
    authors: list[str]
    isbn_10: str | None = None
    isbn_13: str | None = None
    status: ReadingStatus
    publication: PublicationMetadataResponse
    cover_url: str | None = None
    progress: ReadingProgressResponse
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    rating: float | None = None
    notes: str | None = None


class BookListResponse(BaseModel):
    items: list[BookResponse]
    total: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    detail: str
    code: str | None = None
