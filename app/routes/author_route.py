from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.author_schema import (
    AuthorCreateSchema,
    AuthorSchema,
    AuthorUpdateSchema,
)
from app.services.author_service import AuthorService, get_author_service

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/", response_model=list[AuthorSchema])
async def get_authors(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    service: AuthorService = Depends(get_author_service),
):
    return await service.get_all(offset, limit)


@router.get("/{author_id}", response_model=AuthorSchema)
async def get_author(
    author_id: int,
    service: AuthorService = Depends(get_author_service),
):
    db_author = await service.get(author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@router.post("/", response_model=AuthorSchema, status_code=201)
async def create_author(
    author: AuthorCreateSchema,
    service: AuthorService = Depends(get_author_service),
):
    db_author = await service.get_by_name(author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return await service.create(author)


@router.put("/{author_id}", response_model=AuthorSchema)
async def update_author(
    author_id: int,
    author_update: AuthorUpdateSchema,
    service: AuthorService = Depends(get_author_service),
):
    db_author = await service.update(author_id, author_update)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@router.delete("/{author_id}", status_code=204)
async def delete_author(
    author_id: int,
    service: AuthorService = Depends(get_author_service),
):
    success = await service.delete(author_id)

    if not success:
        raise HTTPException(status_code=404, detail="Author not found")

    return None
