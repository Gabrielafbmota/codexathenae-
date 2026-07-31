from __future__ import annotations

import uuid


class BookId:
    """Unique identifier for a Book entity."""

    def __init__(self, value: str) -> None:
        try:
            self._value = str(uuid.UUID(value))
        except ValueError as exc:
            raise ValueError(f"Invalid BookId: '{value}'") from exc

    @classmethod
    def generate(cls) -> BookId:
        return cls(str(uuid.uuid4()))

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BookId):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"BookId({self._value!r})"
