# built-in
import traceback
from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List

# custom
from src.Persistance.database import get_db_session
from src.Models.BookModel import BookModel, BookCountModel
from src.Models.UserModel import UserModel
from src.Models.Borrowings import Borrowings
from src.Schema.BorrowRequestSchema import BorrowRequestSchema
from src.Schema.UserBorrowHistoryResponse import UserBorrowHistoryResponse
from src.Schema.BookSchema import BookSchema

user_router = APIRouter(
    prefix="/{user_id}"
)

def get_user(user_id: int, db_session: Session):
    user = db_session.query(UserModel).filter(UserModel.id == user_id).first()
    return user

def get_book_data(book_id: int, db_session: Session):
    book_obj = db_session.query(BookModel).join(BookCountModel, BookModel.id == BookCountModel.id).filter(BookModel.id == book_id).first()
    return book_obj

def get_borrow_history(user_id: int, db_session: Session):
    history_data = db_session.query(Borrowings).join(BookModel, Borrowings.book_id == BookModel.id).filter(Borrowings.user_id == user_id).all()
    return history_data

def get_all_books_in_db(db_session: Session):
    all_books = db_session.query(BookModel).join(BookCountModel, BookModel.id == BookCountModel.id).filter(BookCountModel.count > 0).all()
    return all_books

@user_router.get("/hello")
def hello():
    print(f"In user Hello")


@user_router.post("/borrow")
def book_request(request: Request, user_id: int, borrow_data: BorrowRequestSchema, db_session: Session = Depends(get_db_session)):
    try:
        user = get_user(user_id, db_session)

        if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Invalid user_id: {user_id}"})
        
        book_id = borrow_data.book_id
        
        book_obj = get_book_data(book_id, db_session)

        if not book_obj:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Invalid book_id: {book_id}"})

        if book_obj.book_count.count <= 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"No books available with name: {book_obj.name}"})


        borrowing_obj = Borrowings.Borrowings(from_time=borrow_data.from_time,
                                   to_time=borrow_data.to_time,
                                   book_id=borrow_data.book_id,
                                   user_id=user_id,
                                   status="PENDING")
        db_session.add(borrowing_obj)

        new_book_count = BookModel.BookCountModel(id=book_obj.id,
                                                  count=book_obj.book_count.count-1)

        db_session.merge(new_book_count)
        db_session.commit()
    except Exception as e:
        print("Exception", e, traceback.print_exc())


@user_router.get("/borrow", response_model=List[UserBorrowHistoryResponse])
def get_user_borrow_history(request: Request, user_id: int, db_session: Session = Depends(get_db_session)):

    user = get_user(user_id, db_session)

    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Invalid user_id: {user_id}"})

    return get_borrow_history(user_id, db_session)
    

@user_router.get("/books", response_model=List[BookSchema])
def get_all_books(request: Request, user_id: str, db_session: Session = Depends(get_db_session)):
    user = get_user(user_id, db_session)

    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Invalid user_id: {user_id}"})
    
    return get_all_books_in_db(db_session)