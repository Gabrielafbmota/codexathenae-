from __future__ import annotations

from dataclasses import dataclass

from codexathenae.domain.exceptions.book_exceptions import InvalidReadingProgressError


@dataclass(frozen=True)
class ReadingProgress:
    pages_read: int = 0
    total_pages: int | None = None

    def __post_init__(self) -> None:
        if self.pages_read < 0:
            raise InvalidReadingProgressError("Pages read cannot be negative")
        if self.total_pages is not None:
            if self.total_pages < 0:
                raise InvalidReadingProgressError("Total pages cannot be negative")
            if self.pages_read > self.total_pages:
                raise InvalidReadingProgressError(
                    f"Pages read ({self.pages_read}) cannot exceed total pages ({self.total_pages})"
                )

    @property
    def percentage(self) -> float | None:
        if self.total_pages is None or self.total_pages == 0:
            return None
        return round((self.pages_read / self.total_pages) * 100, 1)

    @classmethod
    def from_percentage(cls, percentage: float, total_pages: int) -> ReadingProgress:
        if percentage < 0 or percentage > 100:
            raise InvalidReadingProgressError(
                f"Percentage must be between 0 and 100, got {percentage}"
            )
        pages_read = round((percentage / 100) * total_pages)
        return cls(pages_read=pages_read, total_pages=total_pages)
