"""Open Library API adapter (fallback metadata provider)."""

from __future__ import annotations

import httpx

from codexathenae.infrastructure.external.models import BookCandidate
from codexathenae.infrastructure.external.open_library.normalizer import normalize_book

_BASE_URL = "https://openlibrary.org"


class OpenLibraryClient:
    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._client = http_client

    async def search_by_isbn(self, isbn: str) -> list[BookCandidate]:
        url = f"{_BASE_URL}/isbn/{isbn}.json"
        try:
            response = await self._client.get(url)
            if response.status_code == 404:
                return []
            response.raise_for_status()
        except httpx.HTTPStatusError:
            return []

        data = response.json()
        candidate = normalize_book(data, isbn=isbn)
        return [candidate] if candidate else []

    async def search_by_title(self, title: str, author: str | None = None) -> list[BookCandidate]:
        params: dict[str, str | int] = {"title": title, "limit": 5}
        if author:
            params["author"] = author

        try:
            response = await self._client.get(f"{_BASE_URL}/search.json", params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError:
            return []

        data = response.json()
        docs = data.get("docs") or []
        candidates: list[BookCandidate] = []
        for doc in docs[:5]:
            candidate = _normalize_search_result(doc)
            if candidate:
                candidates.append(candidate)
        return candidates


def _normalize_search_result(doc: dict[str, object]) -> BookCandidate | None:
    title = doc.get("title")
    if not isinstance(title, str) or not title:
        return None
    authors_raw = doc.get("author_name") or []
    authors: list[str] = [a for a in authors_raw if isinstance(a, str)]
    isbns_raw = doc.get("isbn") or []
    isbn_13: str | None = None
    isbn_10: str | None = None
    for isbn in isbns_raw:
        if isinstance(isbn, str):
            if len(isbn) == 13:
                isbn_13 = isbn_13 or isbn
            elif len(isbn) == 10:
                isbn_10 = isbn_10 or isbn
    return BookCandidate(
        source="open_library",
        title=title,
        authors=authors,
        isbn_10=isbn_10,
        isbn_13=isbn_13,
        published_year=(
            int(str(doc.get("first_publish_year"))) if doc.get("first_publish_year") else None
        ),
        page_count=(
            int(str(doc.get("number_of_pages_median")))
            if doc.get("number_of_pages_median")
            else None
        ),
    )
