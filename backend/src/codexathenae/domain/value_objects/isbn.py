from __future__ import annotations

import re

from codexathenae.domain.exceptions.book_exceptions import InvalidISBNError

_STRIP_PATTERN = re.compile(r"[\s\-]")


class ISBN:
    """Normalized, validated ISBN value object (ISBN-10 or ISBN-13)."""

    def __init__(self, raw: str) -> None:
        normalized = _STRIP_PATTERN.sub("", raw).upper()
        if len(normalized) == 10:
            if not _valid_isbn10(normalized):
                raise InvalidISBNError(raw)
            self._value = normalized
            self._kind = "ISBN-10"
        elif len(normalized) == 13:
            if not _valid_isbn13(normalized):
                raise InvalidISBNError(raw)
            self._value = normalized
            self._kind = "ISBN-13"
        else:
            raise InvalidISBNError(raw)

    @property
    def value(self) -> str:
        return self._value

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def is_isbn13(self) -> bool:
        return self._kind == "ISBN-13"

    @property
    def is_isbn10(self) -> bool:
        return self._kind == "ISBN-10"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ISBN):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"ISBN({self._value!r})"


def _valid_isbn10(value: str) -> bool:
    if not re.match(r"^\d{9}[\dX]$", value):
        return False
    total = sum((10 - i) * (10 if c == "X" else int(c)) for i, c in enumerate(value))
    return total % 11 == 0


def _valid_isbn13(value: str) -> bool:
    if not re.match(r"^\d{13}$", value):
        return False
    total = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(value))
    return total % 10 == 0
