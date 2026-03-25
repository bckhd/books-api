from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.book_model import BookModel
from app.schemas.book_schema import BookCreateSchema, BookUpdateSchema


class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, book_id: int):
        query = select(BookModel).where(BookModel.id == book_id)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_all(self, offset: int, limit: int, author_id: int = None):
        query = select(BookModel)

        if author_id:
            query = query.filter(BookModel.author_id == author_id)

        query = query.offset(offset).limit(limit)
        result = await self.db.execute(query)

        return result.scalars().all()

    async def create(self, book: BookCreateSchema):
        db_book = BookModel(**book.model_dump())

        self.db.add(db_book)
        await self.db.commit()
        await self.db.refresh(db_book)

        return db_book

    async def update(self, book_id: int, book_update: BookUpdateSchema):
        db_book = await self.get(book_id)

        if db_book:
            update_data = book_update.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(db_book, field, value)

            await self.db.commit()
            await self.db.refresh(db_book)

        return db_book

    async def delete(self, book_id: int):
        db_book = await self.get(book_id)

        if db_book:
            await self.db.delete(db_book)
            await self.db.commit()

            return True

        return False


async def get_book_service(db: AsyncSession = Depends(get_db)) -> BookService:
    return BookService(db)
