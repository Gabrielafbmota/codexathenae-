"""Canonical metadata candidate returned by external providers."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BookCandidate:
    source: str
    title: str
    authors: list[str] = field(default_factory=list)
    subtitle: str | None = None
    isbn_10: str | None = None
    isbn_13: str | None = None
    publisher: str | None = None
    published_year: int | None = None
    description: str | None = None
    page_count: int | None = None
    genres: list[str] = field(default_factory=list)
    language: str | None = None
    cover_url: str | None = None
