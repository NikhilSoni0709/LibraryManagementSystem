# built-in
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Dict, Union
from typing import List
from datetime import datetime

# custom
from src.Persistance.database import get_db_session
from src.Models.UserModel import UserModel
from src.Models.BookModel import BookModel, BookCountModel
from src.Models.Borrowings import Borrowings
from src.Schema.UserSchema import UserSchema
from src.Routers.UserRouter import get_borrow_history
from src.Schema.UserBorrowHistoryResponse import UserBorrowHistoryResponse, AllUserBorrowHistoryResponse
from src.Schema.ActionRequestSchema import ActionRequestSchema
from src.Security.HashGenerator import HashGenerator
from src.Enums.EnumsClass import BorrowStatus
from src.Routers.UserRouter import *


librarian_router = APIRouter(
    prefix="/admin"
)

def get_all_books(db_session: Session):
    books_obj = db_session.query(BookModel).join(BookCountModel, BookModel.id == BookCountModel.id).all()
    return books_obj

@librarian_router.get("/hello")
def hello():
    print(f"In Hello")


@librarian_router.post("/user")
def add_user(request: Request, user: UserSchema, db_session: Session = Depends(get_db_session)):
    password_hash = HashGenerator.generate(user.password)
    db_session.add(UserModel(name=user.name, password=password_hash, email=user.email, category=user.category))
    db_session.commit()
    print(f"User Added {user}")


@librarian_router.post("/book")
def add_book(requests: Request, book: Dict[str, Union[str, int]], db_session: Session = Depends(get_db_session)):
    new_book = BookModel(name=book["name"], category=book["category"], author_name=book["author_name"], stock=book["count"])
    new_book.book_count = BookCountModel(count=book["count"])
    db_session.add(new_book.book_count)
    db_session.commit()
    db_session.add(new_book)
    db_session.commit()
    print(f"Book Added: {book}")


@librarian_router.get("/book-requests/")
@librarian_router.get("/book-requests/{user_name}")
def get_all_book_requests(request: Request, user_name: str = None, db_session: Session = Depends(get_db_session)):
    try:
        if user_name is None:
            all_user_data = []
            for borrowing, book, user in db_session.query(Borrowings, BookModel, UserModel) \
                                                    .join(BookModel, BookModel.id == Borrowings.book_id) \
                                                    .join(UserModel, UserModel.id == Borrowings.user_id).all():
                if borrowing.status == "PENDING":
                    user_data = AllUserBorrowHistoryResponse(id=borrowing.id,
                                                            book_name=book.name, 
                                                            user_name=user.name,
                                                            ask_from_time=borrowing.ask_from_time,
                                                            ask_to_time=borrowing.ask_to_time,
                                                            status=borrowing.status)  
                    all_user_data.append(user_data)

            return all_user_data
        else:
            result = db_session.query(UserModel.id).filter(UserModel.name == user_name).first()
            user_id = result[0]
            print("DEBUG-> ", user_id)
            if not user_id:
                return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"No such user: {user_name}")
            
            return get_borrow_history(user_id, db_session)
    except Exception as e:
        print(f"Exception: {e}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to get books at this time")


@librarian_router.patch("/book-requests/")
def take_action_for_request(request: Request, action_data: ActionRequestSchema, db_session: Session = Depends(get_db_session)):

    borrow_id = action_data.borrow_id
    action = action_data.action

    if action not in ("APPROVE", "DENY"):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such action allowed")
    
    updated_borrow_entry = db_session.query(Borrowings).filter(Borrowings.id == borrow_id).first()
    
    if updated_borrow_entry is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such borrow request")
    
    updated_borrow_entry.status = BorrowStatus.APPROVED.name if action == "APPROVE" else BorrowStatus.DENIED.name

    if updated_borrow_entry.status == BorrowStatus.APPROVED.name:
        updated_borrow_entry.alloted_from_time = datetime.now()
    
    db_session.merge(updated_borrow_entry)
    db_session.commit()

@librarian_router.patch("/return")
def return_book_with_id(request: Request, book_data: dict, db_session: Session = Depends(get_db_session)):
    book_id = book_data["book_id"]
    book = get_book_data_by_id(book_id, db_session)

    if not book:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"No such book"})
    
    borrowing = db_session.query(Borrowings).filter(and_(Borrowings.user_id==request.state.user_id, Borrowings.book_id==book_id)).first()
    book_count = db_session.query(BookCountModel).filter(BookCountModel.id==book_id).first()
    book_count.count += 1
    borrowing.status = EnumsClass.BorrowStatus.REVIVED.name

    db_session.commit()

@librarian_router.get('/book')
def all_books(request: Request, db_session: Session = Depends(get_db_session)):
    return get_all_books(db_session)

@librarian_router.delete('/book/{book_name}')
def delete_book(request: Request, book_name: str = None, db_session: Session = Depends(get_db_session)):
    book = db_session.query(BookModel).filter(BookModel.name==book_name).first()
    book_count = db_session.query(BookCountModel).filter(BookCountModel.id==book.id).first()
    db_session.delete(book_count)
    db_session.commit()
    db_session.delete(book)
    db_session.commit()