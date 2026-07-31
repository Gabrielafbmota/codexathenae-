"""Unit tests for ReadingProgress value object."""

import pytest

from codexathenae.domain.exceptions.book_exceptions import InvalidReadingProgressError
from codexathenae.domain.value_objects.reading_progress import ReadingProgress


class TestReadingProgress:
    def test_default_zero_progress(self) -> None:
        p = ReadingProgress()
        assert p.pages_read == 0
        assert p.total_pages is None

    def test_valid_progress(self) -> None:
        p = ReadingProgress(pages_read=50, total_pages=200)
        assert p.percentage == 25.0

    def test_negative_pages_raises(self) -> None:
        with pytest.raises(InvalidReadingProgressError):
            ReadingProgress(pages_read=-1)

    def test_pages_exceed_total_raises(self) -> None:
        with pytest.raises(InvalidReadingProgressError):
            ReadingProgress(pages_read=201, total_pages=200)

    def test_from_percentage(self) -> None:
        p = ReadingProgress.from_percentage(50.0, 200)
        assert p.pages_read == 100
        assert p.total_pages == 200

    def test_invalid_percentage_above_100(self) -> None:
        with pytest.raises(InvalidReadingProgressError):
            ReadingProgress.from_percentage(101.0, 200)

    def test_percentage_none_without_total(self) -> None:
        p = ReadingProgress(pages_read=10)
        assert p.percentage is None
