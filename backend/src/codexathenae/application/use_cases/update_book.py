from codexathenae.application.dto.book_dto import BookDTO, UpdateBookCommand
from codexathenae.application.ports.book_repository import BookRepository
from codexathenae.application.use_cases._mapper import book_to_dto
from codexathenae.domain.exceptions.book_exceptions import BookNotFoundError
from codexathenae.domain.value_objects.book_id import BookId
from codexathenae.domain.value_objects.publication_metadata import PublicationMetadata


class UpdateBookUseCase:
    def __init__(self, repository: BookRepository) -> None:
        self._repository = repository

    async def execute(self, command: UpdateBookCommand) -> BookDTO:
        try:
            bid = BookId(command.book_id)
        except ValueError as exc:
            raise BookNotFoundError(command.book_id) from exc

        book = await self._repository.get_by_id(bid)
        if book is None:
            raise BookNotFoundError(command.book_id)

        publication: PublicationMetadata | None = None
        if any(
            f is not None
            for f in [
                command.publisher,
                command.published_year,
                command.page_count,
                command.language,
                command.description,
            ]
        ):
            old = book.publication
            new_publisher = command.publisher if command.publisher is not None else old.publisher
            new_year = (
                command.published_year if command.published_year is not None else old.published_year
            )
            new_pages = command.page_count if command.page_count is not None else old.page_count
            new_lang = command.language if command.language is not None else old.language
            new_desc = command.description if command.description is not None else old.description
            publication = PublicationMetadata(
                publisher=new_publisher,
                published_year=new_year,
                page_count=new_pages,
                language=new_lang,
                description=new_desc,
                subtitle=old.subtitle,
                original_year=old.original_year,
                genres=list(old.genres),
            )

        book.update_metadata(
            title=command.title,
            authors=command.authors,
            publication=publication,
            cover_url=command.cover_url,
        )

        await self._repository.update(book)
        return book_to_dto(book)
