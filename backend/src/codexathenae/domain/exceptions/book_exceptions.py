class DomainError(Exception):
    """Base class for all domain errors."""


class InvalidISBNError(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"Invalid ISBN: '{value}'")
        self.value = value


class DuplicateISBNError(DomainError):
    def __init__(self, isbn: str) -> None:
        super().__init__(f"A book with ISBN '{isbn}' already exists")
        self.isbn = isbn


class BookNotFoundError(DomainError):
    def __init__(self, book_id: str) -> None:
        super().__init__(f"Book not found: '{book_id}'")
        self.book_id = book_id


class BookAlreadyExistsError(DomainError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class InvalidStatusTransitionError(DomainError):
    def __init__(self, from_status: str, to_status: str) -> None:
        super().__init__(f"Cannot transition from '{from_status}' to '{to_status}'")
        self.from_status = from_status
        self.to_status = to_status


class InvalidReadingProgressError(DomainError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class InvalidRatingError(DomainError):
    def __init__(self, value: float) -> None:
        super().__init__(f"Rating must be between 1 and 5 in 0.5 increments, got {value}")
        self.value = value


class MissingCompletionDateError(DomainError):
    def __init__(self) -> None:
        super().__init__("A book cannot be marked as 'read' without a completion date")
