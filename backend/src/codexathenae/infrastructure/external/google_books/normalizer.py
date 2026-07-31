"""Convert a Google Books volume item into our canonical BookCandidate."""

from __future__ import annotations

from typing import Any

from codexathenae.infrastructure.external.models import BookCandidate

_SOURCE = "google_books"


def normalize_volume(item: dict[str, Any]) -> BookCandidate | None:
    info = item.get("volumeInfo") or {}
    title = info.get("title")
    if not title:
        return None

    authors = list(info.get("authors") or [])

    isbn_10: str | None = None
    isbn_13: str | None = None
    for identifier in info.get("industryIdentifiers") or []:
        id_type = identifier.get("type", "")
        id_val = identifier.get("identifier", "")
        if id_type == "ISBN_13":
            isbn_13 = id_val
        elif id_type == "ISBN_10":
            isbn_10 = id_val

    image_links = info.get("imageLinks") or {}
    cover_url = image_links.get("thumbnail") or image_links.get("smallThumbnail")

    return BookCandidate(
        source=_SOURCE,
        title=title,
        subtitle=info.get("subtitle"),
        authors=authors,
        isbn_10=isbn_10,
        isbn_13=isbn_13,
        publisher=info.get("publisher"),
        published_year=_parse_year(info.get("publishedDate")),
        description=info.get("description"),
        page_count=info.get("pageCount"),
        genres=list(info.get("categories") or []),
        language=info.get("language"),
        cover_url=cover_url,
    )


def _parse_year(raw: str | None) -> int | None:
    if not raw:
        return None
    try:
        return int(raw[:4])
    except (ValueError, TypeError):
        return None
