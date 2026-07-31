from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status

from codexathenae.application.dto.book_dto import (
    BookQueryFilters,
    CreateBookCommand,
    UpdateBookCommand,
)
from codexathenae.application.use_cases import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookUseCase,
    ListBooksUseCase,
    UpdateBookUseCase,
)
from codexathenae.domain.enums.reading_status import ReadingStatus
from codexathenae.presentation.api.dependencies import (
    get_create_book_use_case,
    get_delete_book_use_case,
    get_get_book_use_case,
    get_list_books_use_case,
    get_update_book_use_case,
)
from codexathenae.presentation.api.schemas.book_schemas import (
    BookCreateRequest,
    BookListResponse,
    BookResponse,
    BookUpdateRequest,
    PublicationMetadataResponse,
    ReadingProgressResponse,
)

router = APIRouter(prefix="/api/v1/books", tags=["books"])


def _dto_to_response(dto: object) -> BookResponse:
    from codexathenae.application.dto.book_dto import BookDTO

    if not isinstance(dto, BookDTO):
        raise TypeError(f"Expected BookDTO, got {type(dto)}")
    return BookResponse(
        id=dto.id,
        title=dto.title,
        authors=dto.authors,
        isbn_10=dto.isbn_10,
        isbn_13=dto.isbn_13,
        status=dto.status,
        publication=PublicationMetadataResponse(
            publisher=dto.publication.publisher,
            published_year=dto.publication.published_year,
            original_year=dto.publication.original_year,
            language=dto.publication.language,
            page_count=dto.publication.page_count,
            genres=dto.publication.genres,
            description=dto.publication.description,
            subtitle=dto.publication.subtitle,
        ),
        cover_url=dto.cover_url,
        progress=ReadingProgressResponse(
            pages_read=dto.progress.pages_read,
            total_pages=dto.progress.total_pages,
            percentage=dto.progress.percentage,
        ),
        created_at=dto.created_at,
        updated_at=dto.updated_at,
        started_at=dto.started_at,
        finished_at=dto.finished_at,
        rating=dto.rating,
        notes=dto.notes,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponse,
    summary="Create a book",
)
async def create_book(
    body: BookCreateRequest,
    response: Response,
    use_case: Annotated[CreateBookUseCase, Depends(get_create_book_use_case)],
) -> BookResponse:
    command = CreateBookCommand(
        title=body.title,
        authors=body.authors,
        isbn=body.isbn,
        status=body.status,
        publisher=body.publisher,
        published_year=body.published_year,
        page_count=body.page_count,
        language=body.language,
        description=body.description,
        cover_url=body.cover_url,
    )
    dto = await use_case.execute(command)
    response.headers["Location"] = f"/api/v1/books/{dto.id}"
    return _dto_to_response(dto)


@router.get(
    "",
    response_model=BookListResponse,
    summary="List books",
)
async def list_books(
    use_case: Annotated[ListBooksUseCase, Depends(get_list_books_use_case)],
    status_filter: Annotated[ReadingStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> BookListResponse:
    filters = BookQueryFilters(status=status_filter, limit=limit, offset=offset)
    result = await use_case.execute(filters)
    return BookListResponse(
        items=[_dto_to_response(item) for item in result.items],
        total=result.total,
        limit=result.limit,
        offset=result.offset,
    )


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get a book by ID",
)
async def get_book(
    book_id: str,
    use_case: Annotated[GetBookUseCase, Depends(get_get_book_use_case)],
) -> BookResponse:
    dto = await use_case.execute(book_id)
    return _dto_to_response(dto)


@router.patch(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update book metadata",
)
async def update_book(
    book_id: str,
    body: BookUpdateRequest,
    use_case: Annotated[UpdateBookUseCase, Depends(get_update_book_use_case)],
) -> BookResponse:
    command = UpdateBookCommand(
        book_id=book_id,
        title=body.title,
        authors=body.authors,
        publisher=body.publisher,
        published_year=body.published_year,
        page_count=body.page_count,
        language=body.language,
        description=body.description,
        cover_url=body.cover_url,
    )
    dto = await use_case.execute(command)
    return _dto_to_response(dto)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete a book",
)
async def delete_book(
    book_id: str,
    use_case: Annotated[DeleteBookUseCase, Depends(get_delete_book_use_case)],
) -> None:
    await use_case.execute(book_id)
