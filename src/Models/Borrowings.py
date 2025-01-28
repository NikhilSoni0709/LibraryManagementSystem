# built-in
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

# custom
from src.Persistance.database import Base, db_engine


class Borrowings(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    possession_time = Column(Integer)  # Adjust data type as needed
    alloted_from_time = Column(DateTime)  # Adjust data type as needed
    alloted_to_time = Column(DateTime)  # Adjust data type as needed
    ask_from_time = Column(DateTime)
    ask_to_time = Column(DateTime)
    status = Column(String)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    book = relationship("BookModel", back_populates="borrowings")
    user = relationship("UserModel", back_populates="borrowings")