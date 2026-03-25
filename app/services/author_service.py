from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.author_model import AuthorModel
from app.schemas.author_schema import AuthorCreateSchema, AuthorUpdateSchema


class AuthorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, author_id: int):
        query = select(AuthorModel).where(AuthorModel.id == author_id)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_name(self, author_name: str):
        query = select(AuthorModel).where(AuthorModel.name == author_name)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_all(self, offset: int, limit: int):
        query = select(AuthorModel).offset(offset).limit(limit)
        result = await self.db.execute(query)

        return result.scalars().all()

    async def create(self, author: AuthorCreateSchema):
        db_author = AuthorModel(**author.model_dump())

        self.db.add(db_author)
        await self.db.commit()
        await self.db.refresh(db_author)

        return db_author

    async def update(self, author_id: int, author_update: AuthorUpdateSchema):
        db_author = await self.get(author_id)

        if db_author:
            update_data = author_update.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(db_author, field, value)

            await self.db.commit()
            await self.db.refresh(db_author)

        return db_author

    async def delete(self, author_id: int):
        db_author = await self.get(author_id)

        if db_author:
            await self.db.delete(db_author)
            await self.db.commit()

            return True

        return False


async def get_author_service(db: AsyncSession = Depends(get_db)) -> AuthorService:
    return AuthorService(db)
