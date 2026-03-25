from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String)
    price = Column(Float)

    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))

    author = relationship("AuthorModel", back_populates="books")
