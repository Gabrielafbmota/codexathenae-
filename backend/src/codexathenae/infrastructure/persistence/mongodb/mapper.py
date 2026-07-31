"""Bidirectional mapper between Book entity and MongoDB documents."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from codexathenae.domain.entities.book import Book
from codexathenae.domain.enums.reading_status import ReadingStatus
from codexathenae.domain.value_objects.book_id import BookId
from codexathenae.domain.value_objects.enrichment_state import EnrichmentState, EnrichmentStatus
from codexathenae.domain.value_objects.isbn import ISBN
from codexathenae.domain.value_objects.publication_metadata import PublicationMetadata
from codexathenae.domain.value_objects.reading_progress import ReadingProgress


def book_to_document(book: Book) -> dict[str, Any]:
    return {
        "_id": book.id.value,
        "title": book.title,
        "authors": book.authors,
        "isbn_10": book.isbn_10.value if book.isbn_10 else None,
        "isbn_13": book.isbn_13.value if book.isbn_13 else None,
        "status": book.status.value,
        "cover_url": book.cover_url,
        "publication": {
            "publisher": book.publication.publisher,
            "published_year": book.publication.published_year,
            "original_year": book.publication.original_year,
            "language": book.publication.language,
            "page_count": book.publication.page_count,
            "genres": list(book.publication.genres),
            "description": book.publication.description,
            "subtitle": book.publication.subtitle,
        },
        "progress": {
            "pages_read": book.progress.pages_read,
            "total_pages": book.progress.total_pages,
        },
        "enrichment": {
            "status": book.enrichment.status.value,
            "source": book.enrichment.source,
            "enriched_at": book.enrichment.enriched_at,
            "confirmed_at": book.enrichment.confirmed_at,
            "field_sources": book.enrichment.field_sources,
            "error_message": book.enrichment.error_message,
        },
        "created_at": book.created_at,
        "updated_at": book.updated_at,
        "started_at": book.started_at,
        "finished_at": book.finished_at,
        "rating": book.rating,
        "notes": book.notes,
        "deleted_at": book.deleted_at,
    }


def document_to_book(doc: dict[str, Any]) -> Book:
    pub_raw = doc.get("publication") or {}
    prog_raw = doc.get("progress") or {}
    enr_raw = doc.get("enrichment") or {}

    publication = PublicationMetadata(
        publisher=pub_raw.get("publisher"),
        published_year=pub_raw.get("published_year"),
        original_year=pub_raw.get("original_year"),
        language=pub_raw.get("language"),
        page_count=pub_raw.get("page_count"),
        genres=list(pub_raw.get("genres") or []),
        description=pub_raw.get("description"),
        subtitle=pub_raw.get("subtitle"),
    )

    progress = ReadingProgress(
        pages_read=prog_raw.get("pages_read", 0),
        total_pages=prog_raw.get("total_pages"),
    )

    enrichment = EnrichmentState(
        status=EnrichmentStatus(enr_raw.get("status", EnrichmentStatus.PENDING.value)),
        source=enr_raw.get("source"),
        enriched_at=_ensure_utc(enr_raw.get("enriched_at")),
        confirmed_at=_ensure_utc(enr_raw.get("confirmed_at")),
        field_sources=dict(enr_raw.get("field_sources") or {}),
        error_message=enr_raw.get("error_message"),
    )

    isbn_10_raw = doc.get("isbn_10")
    isbn_13_raw = doc.get("isbn_13")

    return Book(
        id=BookId(doc["_id"]),
        title=doc["title"],
        authors=list(doc.get("authors") or []),
        isbn_10=ISBN(isbn_10_raw) if isbn_10_raw else None,
        isbn_13=ISBN(isbn_13_raw) if isbn_13_raw else None,
        status=ReadingStatus(doc["status"]),
        publication=publication,
        cover_url=doc.get("cover_url"),
        progress=progress,
        enrichment=enrichment,
        created_at=_ensure_utc(doc["created_at"]),
        updated_at=_ensure_utc(doc["updated_at"]),
        started_at=_ensure_utc(doc.get("started_at")),
        finished_at=_ensure_utc(doc.get("finished_at")),
        rating=doc.get("rating"),
        notes=doc.get("notes"),
        deleted_at=_ensure_utc(doc.get("deleted_at")),
    )


def _ensure_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value
