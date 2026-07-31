from codexathenae.application.dto.book_dto import BookDTO, CreateBookCommand
from codexathenae.application.ports.book_repository import BookRepository
from codexathenae.application.use_cases._mapper import book_to_dto
from codexathenae.domain.entities.book import Book
from codexathenae.domain.exceptions.book_exceptions import DuplicateISBNError
from codexathenae.domain.value_objects.isbn import ISBN


class CreateBookUseCase:
    def __init__(self, repository: BookRepository) -> None:
        self._repository = repository

    async def execute(self, command: CreateBookCommand) -> BookDTO:
        isbn_10: ISBN | None = None
        isbn_13: ISBN | None = None

        if command.isbn:
            isbn = ISBN(command.isbn)
            if isbn.is_isbn13:
                isbn_13 = isbn
            else:
                isbn_10 = isbn

            existing = await self._repository.get_by_isbn(isbn)
            if existing is not None:
                raise DuplicateISBNError(isbn.value)

        from codexathenae.domain.value_objects.publication_metadata import PublicationMetadata

        publication = PublicationMetadata(
            publisher=command.publisher,
            published_year=command.published_year,
            page_count=command.page_count,
            language=command.language,
            description=command.description,
        )

        book = Book.create(
            title=command.title,
            authors=command.authors,
            isbn_10=isbn_10,
            isbn_13=isbn_13,
            status=command.status,
            publication=publication,
            cover_url=command.cover_url,
        )

        await self._repository.create(book)
        return book_to_dto(book)
