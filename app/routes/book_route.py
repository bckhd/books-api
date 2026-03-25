from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.book_schema import BookCreateSchema, BookSchema, BookUpdateSchema
from app.services.author_service import AuthorService, get_author_service
from app.services.book_service import BookService, get_book_service

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookSchema])
async def get_books(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    author_id: int | None = None,
    service: BookService = Depends(get_book_service),
):
    return await service.get_all(offset, limit, author_id)


@router.get("/{book_id}", response_model=BookSchema)
async def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    db_book = await service.get(book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@router.post("/", response_model=BookSchema, status_code=201)
async def create_book(
    book: BookCreateSchema,
    book_service: BookService = Depends(get_book_service),
    author_service: AuthorService = Depends(get_author_service),
):
    author = await author_service.get(book.author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return await book_service.create(book)


@router.put("/{book_id}", response_model=BookSchema)
async def update_book(
    book_id: int,
    book_update: BookUpdateSchema,
    book_service: BookService = Depends(get_book_service),
    author_service: AuthorService = Depends(get_author_service),
):
    if book_update.author_id:
        author = await author_service.get(book_update.author_id)

        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

    db_book = await book_service.update(book_id, book_update)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    success = await service.delete(book_id)

    if not success:
        raise HTTPException(status_code=404, detail="Book not found")

    return None
