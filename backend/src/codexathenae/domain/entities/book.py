from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from codexathenae.domain.enums.reading_status import ReadingStatus
from codexathenae.domain.exceptions.book_exceptions import (
    InvalidRatingError,
    InvalidStatusTransitionError,
    MissingCompletionDateError,
)
from codexathenae.domain.value_objects.book_id import BookId
from codexathenae.domain.value_objects.enrichment_state import EnrichmentState, EnrichmentStatus
from codexathenae.domain.value_objects.isbn import ISBN
from codexathenae.domain.value_objects.publication_metadata import PublicationMetadata
from codexathenae.domain.value_objects.reading_progress import ReadingProgress

if TYPE_CHECKING:
    pass

_RATING_STEPS = {round(v * 0.5, 1) for v in range(2, 11)}  # 1.0 to 5.0 in 0.5 steps


class Book:
    """
    Core domain entity representing a book in the personal library.

    All business invariants are enforced here; no framework dependencies allowed.
    """

    def __init__(
        self,
        *,
        id: BookId,
        title: str,
        authors: list[str],
        isbn_10: ISBN | None,
        isbn_13: ISBN | None,
        status: ReadingStatus,
        publication: PublicationMetadata,
        cover_url: str | None,
        progress: ReadingProgress,
        enrichment: EnrichmentState,
        created_at: datetime,
        updated_at: datetime,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        rating: float | None = None,
        notes: str | None = None,
        deleted_at: datetime | None = None,
    ) -> None:
        self._id = id
        self._title = title
        self._authors = list(authors)
        self._isbn_10 = isbn_10
        self._isbn_13 = isbn_13
        self._status = status
        self._publication = publication
        self._cover_url = cover_url
        self._progress = progress
        self._enrichment = enrichment
        self._created_at = created_at
        self._updated_at = updated_at
        self._started_at = started_at
        self._finished_at = finished_at
        self._rating = rating
        self._notes = notes
        self._deleted_at = deleted_at

    @classmethod
    def create(
        cls,
        *,
        title: str,
        authors: list[str],
        isbn_10: ISBN | None = None,
        isbn_13: ISBN | None = None,
        status: ReadingStatus = ReadingStatus.WANT_TO_READ,
        publication: PublicationMetadata | None = None,
        cover_url: str | None = None,
    ) -> Book:
        now = datetime.now(UTC)
        return cls(
            id=BookId.generate(),
            title=title,
            authors=authors,
            isbn_10=isbn_10,
            isbn_13=isbn_13,
            status=status,
            publication=publication or PublicationMetadata(),
            cover_url=cover_url,
            progress=ReadingProgress(),
            enrichment=EnrichmentState(),
            created_at=now,
            updated_at=now,
        )

    # ── Accessors ────────────────────────────────────────────────────────────

    @property
    def id(self) -> BookId:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def authors(self) -> list[str]:
        return list(self._authors)

    @property
    def isbn_10(self) -> ISBN | None:
        return self._isbn_10

    @property
    def isbn_13(self) -> ISBN | None:
        return self._isbn_13

    @property
    def status(self) -> ReadingStatus:
        return self._status

    @property
    def publication(self) -> PublicationMetadata:
        return self._publication

    @property
    def cover_url(self) -> str | None:
        return self._cover_url

    @property
    def progress(self) -> ReadingProgress:
        return self._progress

    @property
    def enrichment(self) -> EnrichmentState:
        return self._enrichment

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def started_at(self) -> datetime | None:
        return self._started_at

    @property
    def finished_at(self) -> datetime | None:
        return self._finished_at

    @property
    def rating(self) -> float | None:
        return self._rating

    @property
    def notes(self) -> str | None:
        return self._notes

    @property
    def deleted_at(self) -> datetime | None:
        return self._deleted_at

    @property
    def is_deleted(self) -> bool:
        return self._deleted_at is not None

    def primary_isbn(self) -> ISBN | None:
        return self._isbn_13 or self._isbn_10

    # ── Behaviour ────────────────────────────────────────────────────────────

    def change_status(self, new_status: ReadingStatus) -> None:
        if not self._status.can_transition_to(new_status):
            raise InvalidStatusTransitionError(self._status, new_status)

        now = datetime.now(UTC)

        if new_status == ReadingStatus.READING and self._started_at is None:
            self._started_at = now

        if new_status == ReadingStatus.READ:
            self._finished_at = now

        self._status = new_status
        self._updated_at = now

    def update_progress(self, progress: ReadingProgress) -> None:
        self._progress = progress
        self._updated_at = datetime.now(UTC)

    def rate(self, rating: float) -> None:
        if rating not in _RATING_STEPS:
            raise InvalidRatingError(rating)
        self._rating = rating
        self._updated_at = datetime.now(UTC)

    def update_notes(self, notes: str) -> None:
        self._notes = notes
        self._updated_at = datetime.now(UTC)

    def soft_delete(self) -> None:
        self._deleted_at = datetime.now(UTC)
        self._updated_at = self._deleted_at

    def update_metadata(
        self,
        *,
        title: str | None = None,
        authors: list[str] | None = None,
        publication: PublicationMetadata | None = None,
        cover_url: str | None = None,
    ) -> None:
        if title is not None:
            self._title = title
        if authors is not None:
            self._authors = list(authors)
        if publication is not None:
            self._publication = publication
        if cover_url is not None:
            self._cover_url = cover_url
        self._updated_at = datetime.now(UTC)

    def confirm_enrichment(
        self,
        *,
        source: str,
        publication: PublicationMetadata | None = None,
        cover_url: str | None = None,
        field_sources: dict[str, str] | None = None,
    ) -> None:
        """Apply externally-fetched metadata only after explicit user confirmation."""
        now = datetime.now(UTC)
        if publication is not None:
            self._publication = publication
        if cover_url is not None:
            self._cover_url = cover_url
        self._enrichment = EnrichmentState(
            status=EnrichmentStatus.CONFIRMED,
            source=source,
            confirmed_at=now,
            field_sources=field_sources or {},
        )
        self._updated_at = now

    def mark_enrichment_completed(self, source: str) -> None:
        now = datetime.now(UTC)
        self._enrichment = EnrichmentState(
            status=EnrichmentStatus.COMPLETED,
            source=source,
            enriched_at=now,
        )
        self._updated_at = now

    def mark_enrichment_failed(self, error_message: str) -> None:
        now = datetime.now(UTC)
        self._enrichment = EnrichmentState(
            status=EnrichmentStatus.FAILED,
            error_message=error_message,
        )
        self._updated_at = now

    def _require_completion_date(self) -> None:
        if self._finished_at is None:
            raise MissingCompletionDateError()

    def __repr__(self) -> str:
        return f"Book(id={self._id!r}, title={self._title!r}, status={self._status!r})"
