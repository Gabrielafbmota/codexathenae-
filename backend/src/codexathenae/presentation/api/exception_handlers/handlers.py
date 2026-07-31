from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from codexathenae.domain.exceptions.book_exceptions import (
    BookNotFoundError,
    DuplicateISBNError,
    InvalidISBNError,
    InvalidRatingError,
    InvalidReadingProgressError,
    InvalidStatusTransitionError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidISBNError)
    async def handle_invalid_isbn(_: Request, exc: InvalidISBNError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"detail": str(exc), "code": "INVALID_ISBN"},
        )

    @app.exception_handler(DuplicateISBNError)
    async def handle_duplicate_isbn(_: Request, exc: DuplicateISBNError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc), "code": "DUPLICATE_ISBN"},
        )

    @app.exception_handler(BookNotFoundError)
    async def handle_book_not_found(_: Request, exc: BookNotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc), "code": "BOOK_NOT_FOUND"},
        )

    @app.exception_handler(InvalidStatusTransitionError)
    async def handle_invalid_transition(
        _: Request, exc: InvalidStatusTransitionError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"detail": str(exc), "code": "INVALID_STATUS_TRANSITION"},
        )

    @app.exception_handler(InvalidReadingProgressError)
    async def handle_invalid_progress(_: Request, exc: InvalidReadingProgressError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"detail": str(exc), "code": "INVALID_PROGRESS"},
        )

    @app.exception_handler(InvalidRatingError)
    async def handle_invalid_rating(_: Request, exc: InvalidRatingError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"detail": str(exc), "code": "INVALID_RATING"},
        )
