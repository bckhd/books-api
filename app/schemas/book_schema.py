from pydantic import BaseModel, ConfigDict, Field


class BookBaseSchema(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = None
    price: float | None = Field(None, ge=0)

    author_id: int


class BookCreateSchema(BookBaseSchema):
    pass


class BookUpdateSchema(BaseModel):
    title: str | None = Field(None, min_length=1)
    description: str | None = None
    price: float | None = Field(None, ge=0)

    author_id: int | None = None


class BookSchema(BookBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
