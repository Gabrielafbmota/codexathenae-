from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class EnrichmentStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CONFIRMED = "confirmed"


@dataclass(frozen=True)
class EnrichmentState:
    status: EnrichmentStatus = EnrichmentStatus.PENDING
    source: str | None = None
    enriched_at: datetime | None = None
    confirmed_at: datetime | None = None
    field_sources: dict[str, str] = field(default_factory=dict)
    error_message: str | None = None
