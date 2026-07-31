from codexathenae.application.dto.book_dto import BookDTO
from codexathenae.application.ports.book_repository import BookRepository
from codexathenae.application.use_cases._mapper import book_to_dto
from codexathenae.domain.exceptions.book_exceptions import BookNotFoundError
from codexathenae.domain.value_objects.book_id import BookId


class GetBookUseCase:
    def __init__(self, repository: BookRepository) -> None:
        self._repository = repository

    async def execute(self, book_id: str) -> BookDTO:
        try:
            bid = BookId(book_id)
        except ValueError as exc:
            raise BookNotFoundError(book_id) from exc

        book = await self._repository.get_by_id(bid)
        if book is None:
            raise BookNotFoundError(book_id)
        return book_to_dto(book)
