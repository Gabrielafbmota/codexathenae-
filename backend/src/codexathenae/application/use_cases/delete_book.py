from codexathenae.application.ports.book_repository import BookRepository
from codexathenae.domain.exceptions.book_exceptions import BookNotFoundError
from codexathenae.domain.value_objects.book_id import BookId


class DeleteBookUseCase:
    def __init__(self, repository: BookRepository) -> None:
        self._repository = repository

    async def execute(self, book_id: str) -> None:
        try:
            bid = BookId(book_id)
        except ValueError as exc:
            raise BookNotFoundError(book_id) from exc

        await self._repository.soft_delete(bid)
