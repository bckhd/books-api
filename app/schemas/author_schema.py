from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class AuthorBaseSchema(BaseModel):
    name: str = Field(..., min_length=1)
    birth_date: date | None = None


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=1)
    birth_date: date | None = None


class AuthorSchema(AuthorBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
