"""Shared helper: convert Book entity → BookDTO."""

from codexathenae.application.dto.book_dto import (
    BookDTO,
    PublicationMetadataDTO,
    ReadingProgressDTO,
)
from codexathenae.domain.entities.book import Book


def book_to_dto(book: Book) -> BookDTO:
    pub = book.publication
    prog = book.progress
    return BookDTO(
        id=book.id.value,
        title=book.title,
        authors=book.authors,
        isbn_10=book.isbn_10.value if book.isbn_10 else None,
        isbn_13=book.isbn_13.value if book.isbn_13 else None,
        status=book.status,
        publication=PublicationMetadataDTO(
            publisher=pub.publisher,
            published_year=pub.published_year,
            original_year=pub.original_year,
            language=pub.language,
            page_count=pub.page_count,
            genres=list(pub.genres),
            description=pub.description,
            subtitle=pub.subtitle,
        ),
        cover_url=book.cover_url,
        progress=ReadingProgressDTO(
            pages_read=prog.pages_read,
            total_pages=prog.total_pages,
            percentage=prog.percentage,
        ),
        created_at=book.created_at,
        updated_at=book.updated_at,
        started_at=book.started_at,
        finished_at=book.finished_at,
        rating=book.rating,
        notes=book.notes,
    )
