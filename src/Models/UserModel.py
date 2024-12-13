# built-in
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship

# custom
from src.Persistance.database import Base, db_engine


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    category = Column(String)

    borrowings = relationship("Borrowings", back_populates="user")
