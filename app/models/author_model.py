from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class AuthorModel(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    birth_date = Column(Date)

    books = relationship(
        "BookModel",
        back_populates="author",
        cascade="all, delete-orphan",
    )
