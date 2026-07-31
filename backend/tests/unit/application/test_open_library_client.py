"""Unit tests for OpenLibraryClient using httpx MockTransport."""

from __future__ import annotations

import httpx
import pytest

from codexathenae.infrastructure.external.models import BookCandidate
from codexathenae.infrastructure.external.open_library.client import OpenLibraryClient

_BOOK_RESPONSE = {
    "title": "Clean Code",
    "authors": [{"name": "Robert C. Martin"}],
    "publishers": ["Prentice Hall"],
    "publish_date": "2008",
    "number_of_pages": 431,
}

_SEARCH_RESPONSE = {
    "numFound": 1,
    "docs": [
        {
            "title": "Clean Code",
            "author_name": ["Robert C. Martin"],
            "isbn": ["9780132350884", "0132350882"],
            "first_publish_year": 2008,
            "number_of_pages_median": 431,
        }
    ],
}


def _make_client_isbn(
    response_data: dict[object, object], status_code: int = 200
) -> OpenLibraryClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json=response_data)

    transport = httpx.MockTransport(handler)
    http_client = httpx.AsyncClient(transport=transport, timeout=5.0)
    return OpenLibraryClient(http_client)


def _make_client_search(
    isbn_response: dict[object, object],
    search_response: dict[object, object],
    isbn_status: int = 200,
) -> OpenLibraryClient:
    def handler(request: httpx.Request) -> httpx.Response:
        if "/isbn/" in str(request.url):
            return httpx.Response(isbn_status, json=isbn_response)
        return httpx.Response(200, json=search_response)

    transport = httpx.MockTransport(handler)
    http_client = httpx.AsyncClient(transport=transport, timeout=5.0)
    return OpenLibraryClient(http_client)


class TestOpenLibrarySearchByISBN:
    @pytest.mark.anyio
    async def test_returns_candidate_for_isbn13(self) -> None:
        client = _make_client_isbn(_BOOK_RESPONSE)
        results = await client.search_by_isbn("9780132350884")
        assert len(results) == 1
        c = results[0]
        assert isinstance(c, BookCandidate)
        assert c.title == "Clean Code"
        assert c.isbn_13 == "9780132350884"
        assert c.source == "open_library"

    @pytest.mark.anyio
    async def test_returns_candidate_for_isbn10(self) -> None:
        client = _make_client_isbn(_BOOK_RESPONSE)
        results = await client.search_by_isbn("0132350882")
        assert len(results) == 1
        c = results[0]
        assert c.isbn_10 == "0132350882"

    @pytest.mark.anyio
    async def test_returns_empty_for_404(self) -> None:
        client = _make_client_isbn({}, status_code=404)
        results = await client.search_by_isbn("9780000000000")
        assert results == []

    @pytest.mark.anyio
    async def test_returns_empty_for_missing_title(self) -> None:
        client = _make_client_isbn({"authors": [{"name": "Author"}]})
        results = await client.search_by_isbn("9780132350884")
        assert results == []

    @pytest.mark.anyio
    async def test_normalizes_publisher_and_year(self) -> None:
        client = _make_client_isbn(_BOOK_RESPONSE)
        results = await client.search_by_isbn("9780132350884")
        c = results[0]
        assert c.publisher == "Prentice Hall"
        assert c.published_year == 2008
        assert c.page_count == 431


class TestOpenLibrarySearchByTitle:
    @pytest.mark.anyio
    async def test_search_by_title_returns_candidates(self) -> None:
        client = _make_client_search({}, _SEARCH_RESPONSE)
        results = await client.search_by_title("Clean Code")
        assert len(results) == 1
        assert results[0].title == "Clean Code"
        assert results[0].isbn_13 == "9780132350884"

    @pytest.mark.anyio
    async def test_search_by_title_and_author(self) -> None:
        client = _make_client_search({}, _SEARCH_RESPONSE)
        results = await client.search_by_title("Clean Code", author="Martin")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_search_returns_empty_for_http_error(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500)

        transport = httpx.MockTransport(handler)
        http_client = httpx.AsyncClient(transport=transport, timeout=5.0)
        client = OpenLibraryClient(http_client)
        results = await client.search_by_title("anything")
        assert results == []
