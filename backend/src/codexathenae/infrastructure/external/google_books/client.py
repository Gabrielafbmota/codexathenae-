"""Google Books API adapter implementing BookMetadataProvider."""

from __future__ import annotations

import httpx

from codexathenae.infrastructure.external.google_books.normalizer import normalize_volume
from codexathenae.infrastructure.external.models import BookCandidate

_BASE_URL = "https://www.googleapis.com/books/v1/volumes"


class GoogleBooksClient:
    def __init__(
        self,
        http_client: httpx.AsyncClient,
        *,
        api_key: str | None = None,
        max_results: int = 5,
    ) -> None:
        self._client = http_client
        self._api_key = api_key
        self._max_results = max(1, min(max_results, 40))

    async def search_by_isbn(self, isbn: str) -> list[BookCandidate]:
        return await self._query(f"isbn:{isbn}")

    async def search_by_title_and_author(
        self, title: str, author: str | None = None
    ) -> list[BookCandidate]:
        q = f'intitle:"{title}"'
        if author:
            q += f'+inauthor:"{author}"'
        return await self._query(q)

    async def _query(self, q: str) -> list[BookCandidate]:
        params: dict[str, str | int] = {
            "q": q,
            "maxResults": self._max_results,
            "printType": "books",
        }
        if self._api_key:
            params["key"] = self._api_key

        response = await self._client.get(_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        items = data.get("items") or []
        candidates: list[BookCandidate] = []
        for item in items:
            candidate = normalize_volume(item)
            if candidate is not None:
                candidates.append(candidate)
        return candidates
