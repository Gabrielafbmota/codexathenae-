from codexathenae.application.dto.book_dto import BookListDTO, BookQueryFilters
from codexathenae.application.ports.book_repository import BookRepository

_MAX_LIMIT = 100


class ListBooksUseCase:
    def __init__(self, repository: BookRepository) -> None:
        self._repository = repository

    async def execute(self, filters: BookQueryFilters) -> BookListDTO:
        effective_filters = BookQueryFilters(
            status=filters.status,
            include_deleted=filters.include_deleted,
            limit=min(filters.limit, _MAX_LIMIT),
            offset=max(filters.offset, 0),
        )
        return await self._repository.list(effective_filters)
