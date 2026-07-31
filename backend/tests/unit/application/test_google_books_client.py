"""Unit tests for GoogleBooksClient using httpx MockTransport."""

from __future__ import annotations

import httpx
import pytest

from codexathenae.infrastructure.external.google_books.client import GoogleBooksClient
from codexathenae.infrastructure.external.models import BookCandidate

_VOLUME_RESPONSE = {
    "kind": "books#volumes",
    "totalItems": 1,
    "items": [
        {
            "kind": "books#volume",
            "id": "abc123",
            "volumeInfo": {
                "title": "Clean Code",
                "subtitle": "A Handbook of Agile Software Craftsmanship",
                "authors": ["Robert C. Martin"],
                "publisher": "Prentice Hall",
                "publishedDate": "2008-08-01",
                "description": "A good book about clean code.",
                "industryIdentifiers": [
                    {"type": "ISBN_13", "identifier": "9780132350884"},
                    {"type": "ISBN_10", "identifier": "0132350882"},
                ],
                "pageCount": 431,
                "categories": ["Computers"],
                "language": "en",
                "imageLinks": {
                    "thumbnail": "http://example.com/cover.jpg",
                },
            },
        }
    ],
}


def _make_client(response_data: dict[object, object], status_code: int = 200) -> GoogleBooksClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json=response_data)

    transport = httpx.MockTransport(handler)
    http_client = httpx.AsyncClient(transport=transport, timeout=5.0)
    return GoogleBooksClient(http_client, max_results=5)


class TestGoogleBooksSearchByISBN:
    @pytest.mark.anyio
    async def test_returns_candidates_for_isbn(self) -> None:
        client = _make_client(_VOLUME_RESPONSE)
        results = await client.search_by_isbn("9780132350884")
        assert len(results) == 1
        candidate = results[0]
        assert isinstance(candidate, BookCandidate)
        assert candidate.title == "Clean Code"
        assert candidate.isbn_13 == "9780132350884"
        assert candidate.isbn_10 == "0132350882"
        assert candidate.source == "google_books"

    @pytest.mark.anyio
    async def test_returns_empty_for_no_items(self) -> None:
        client = _make_client({"kind": "books#volumes", "totalItems": 0})
        results = await client.search_by_isbn("0000000000000")
        assert results == []

    @pytest.mark.anyio
    async def test_normalizes_fields_correctly(self) -> None:
        client = _make_client(_VOLUME_RESPONSE)
        results = await client.search_by_isbn("9780132350884")
        c = results[0]
        assert c.authors == ["Robert C. Martin"]
        assert c.publisher == "Prentice Hall"
        assert c.published_year == 2008
        assert c.page_count == 431
        assert c.language == "en"
        assert c.cover_url == "http://example.com/cover.jpg"
        assert c.subtitle == "A Handbook of Agile Software Craftsmanship"

    @pytest.mark.anyio
    async def test_returns_empty_list_not_error_on_empty_title(self) -> None:
        data = {"items": [{"volumeInfo": {"authors": ["Author"]}}]}
        client = _make_client(data)
        results = await client.search_by_isbn("9780132350884")
        assert results == []


class TestGoogleBooksSearchByTitle:
    @pytest.mark.anyio
    async def test_search_by_title(self) -> None:
        client = _make_client(_VOLUME_RESPONSE)
        results = await client.search_by_title_and_author("Clean Code", "Martin")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_search_by_title_without_author(self) -> None:
        client = _make_client(_VOLUME_RESPONSE)
        results = await client.search_by_title_and_author("Clean Code")
        assert len(results) == 1
