from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PublicationMetadata:
    publisher: str | None = None
    published_year: int | None = None
    original_year: int | None = None
    language: str | None = None
    page_count: int | None = None
    genres: list[str] = field(default_factory=list)
    description: str | None = None
    subtitle: str | None = None
