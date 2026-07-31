"""Normalize Open Library book record to BookCandidate."""

from __future__ import annotations

import contextlib
from typing import Any

from codexathenae.infrastructure.external.models import BookCandidate


def normalize_book(data: dict[str, Any], isbn: str | None = None) -> BookCandidate | None:
    title = data.get("title")
    if not isinstance(title, str) or not title:
        return None

    authors: list[str] = []
    for author_ref in data.get("authors") or []:
        if isinstance(author_ref, dict):
            name = author_ref.get("name") or author_ref.get("key", "")
            if name:
                authors.append(str(name))

    isbn_13: str | None = None
    isbn_10: str | None = None
    if isbn:
        if len(isbn) == 13:
            isbn_13 = isbn
        elif len(isbn) == 10:
            isbn_10 = isbn

    publishers_raw = data.get("publishers") or []
    publisher: str | None = None
    if publishers_raw and isinstance(publishers_raw[0], str):
        publisher = publishers_raw[0]

    publish_date: str | None = data.get("publish_date")
    published_year: int | None = None
    if publish_date:
        with contextlib.suppress(ValueError, TypeError):
            published_year = int(str(publish_date)[-4:])

    page_count_raw = data.get("number_of_pages")
    page_count: int | None = int(str(page_count_raw)) if page_count_raw else None

    return BookCandidate(
        source="open_library",
        title=title,
        authors=authors,
        isbn_10=isbn_10,
        isbn_13=isbn_13,
        publisher=publisher,
        published_year=published_year,
        page_count=page_count,
    )
