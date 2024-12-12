# built-in
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from typing import Dict, Union

# custom
from src.Persistance.database import get_db_session
from src.Models.UserModel import UserModel
from src.Models.BookModel import BookModel, BookCountModel
from src.Schema.UserSchema import UserSchema
from src.Security.HashGenerator import HashGenerator

librarian_router = APIRouter(
    prefix="/admin"
)

@librarian_router.get("/hello")
def hello():
    print(f"In Hello")


@librarian_router.post("/user")
def add_user(request: Request, user: UserSchema, db_session: Session = Depends(get_db_session)):
    print(user)
    password_hash = HashGenerator.generate(user.password)
    db_session.add(UserModel(name=user.name, password=password_hash, email=user.email))
    db_session.commit()
    print(f"User Added")


@librarian_router.post("/book")
def add_book(requests: Request, book: Dict[str, Union[str, int]], db_session: Session = Depends(get_db_session)):
    print(book)
    new_book = BookModel(name=book["name"], category=book["category"])
    new_book.book_count = BookCountModel(count=book["count"])
    db_session.add(new_book)
    db_session.commit()
    print(f"Book Added: {book}")
