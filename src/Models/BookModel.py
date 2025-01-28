# built-in
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship

# custom
from src.Persistance.database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    author_name = Column(String)
    stock = Column(Integer)
    book_count = relationship("BookCountModel", uselist=False, back_populates="book")
    borrowings = relationship("Borrowings", back_populates="book")

    
class BookCountModel(Base):
    __tablename__ = "books_count"

    id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    count = Column(Integer)
    book = relationship("BookModel", back_populates="book_count")
