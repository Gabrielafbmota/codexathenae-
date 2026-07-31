"""Unit tests for Book entity."""

from datetime import UTC

import pytest

from codexathenae.domain.entities.book import Book
from codexathenae.domain.enums.reading_status import ReadingStatus
from codexathenae.domain.exceptions.book_exceptions import (
    InvalidRatingError,
    InvalidStatusTransitionError,
)
from codexathenae.domain.value_objects.isbn import ISBN
from codexathenae.domain.value_objects.reading_progress import ReadingProgress


def _make_book(**kwargs: object) -> Book:
    defaults = {
        "title": "Clean Code",
        "authors": ["Robert C. Martin"],
    }
    defaults.update(kwargs)
    return Book.create(**defaults)  # type: ignore[arg-type]


class TestBookCreation:
    def test_creates_book_with_defaults(self) -> None:
        book = _make_book()
        assert book.title == "Clean Code"
        assert book.status == ReadingStatus.WANT_TO_READ
        assert book.isbn_10 is None
        assert book.isbn_13 is None
        assert not book.is_deleted

    def test_creates_book_with_isbn13(self) -> None:
        book = _make_book(isbn_13=ISBN("9780306406157"))
        assert book.isbn_13 is not None
        assert book.isbn_13.value == "9780306406157"

    def test_creates_book_with_isbn10(self) -> None:
        book = _make_book(isbn_10=ISBN("0306406152"))
        assert book.isbn_10 is not None

    def test_id_is_generated(self) -> None:
        b1 = _make_book()
        b2 = _make_book()
        assert b1.id != b2.id

    def test_timestamps_are_utc(self) -> None:

        book = _make_book()
        assert book.created_at.tzinfo == UTC
        assert book.updated_at.tzinfo == UTC

    def test_no_framework_imports(self) -> None:
        import sys

        for name in list(sys.modules):
            if "fastapi" in name or "pymongo" in name or "pydantic" in name:
                mod = sys.modules[name]
                src = getattr(mod, "__file__", "") or ""
                if "codexathenae/domain" in src:
                    pytest.fail(f"Domain imported {name}")


class TestStatusTransitions:
    def test_want_to_read_to_reading(self) -> None:
        book = _make_book()
        book.change_status(ReadingStatus.READING)
        assert book.status == ReadingStatus.READING
        assert book.started_at is not None

    def test_reading_to_read(self) -> None:
        book = _make_book()
        book.change_status(ReadingStatus.READING)
        book.change_status(ReadingStatus.READ)
        assert book.status == ReadingStatus.READ
        assert book.finished_at is not None

    def test_reading_to_abandoned(self) -> None:
        book = _make_book()
        book.change_status(ReadingStatus.READING)
        book.change_status(ReadingStatus.ABANDONED)
        assert book.status == ReadingStatus.ABANDONED

    def test_abandoned_to_reading(self) -> None:
        book = _make_book()
        book.change_status(ReadingStatus.READING)
        book.change_status(ReadingStatus.ABANDONED)
        book.change_status(ReadingStatus.READING)
        assert book.status == ReadingStatus.READING

    def test_invalid_transition_raises(self) -> None:
        book = _make_book()
        with pytest.raises(InvalidStatusTransitionError):
            book.change_status(ReadingStatus.READ)

    def test_want_to_read_to_abandoned_is_invalid(self) -> None:
        book = _make_book()
        with pytest.raises(InvalidStatusTransitionError):
            book.change_status(ReadingStatus.ABANDONED)


class TestRating:
    def test_valid_rating(self) -> None:
        book = _make_book()
        book.rate(4.5)
        assert book.rating == 4.5

    def test_valid_rating_boundaries(self) -> None:
        book = _make_book()
        book.rate(1.0)
        assert book.rating == 1.0
        book.rate(5.0)
        assert book.rating == 5.0

    def test_invalid_rating_zero(self) -> None:
        book = _make_book()
        with pytest.raises(InvalidRatingError):
            book.rate(0.0)

    def test_invalid_rating_above_five(self) -> None:
        book = _make_book()
        with pytest.raises(InvalidRatingError):
            book.rate(5.5)

    def test_invalid_rating_non_half_increment(self) -> None:
        book = _make_book()
        with pytest.raises(InvalidRatingError):
            book.rate(3.3)


class TestSoftDelete:
    def test_soft_delete_marks_deleted(self) -> None:
        book = _make_book()
        assert not book.is_deleted
        book.soft_delete()
        assert book.is_deleted
        assert book.deleted_at is not None


class TestReadingProgress:
    def test_update_progress(self) -> None:
        book = _make_book()
        progress = ReadingProgress(pages_read=50, total_pages=200)
        book.update_progress(progress)
        assert book.progress.pages_read == 50
        assert book.progress.percentage == 25.0

    def test_progress_percentage_none_without_total(self) -> None:
        progress = ReadingProgress(pages_read=0)
        assert progress.percentage is None
