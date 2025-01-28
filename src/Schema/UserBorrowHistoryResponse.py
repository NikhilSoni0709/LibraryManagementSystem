# built-in
from pydantic import BaseModel, Field
from typing import Union
from datetime import datetime

from src.Schema.BookSchema import BookSchema
from src.Schema.UserSchema import UserSchema

class UserBorrowHistoryResponse(BaseModel):
    id: Union[int, None] = Field(alias="id")
    book: Union[BookSchema, None] = None
    ask_from_time: Union[datetime, None] = None
    ask_to_time: Union[datetime, None] = None
    alloted_from_time: Union[datetime, None] = None
    alloted_to_time: Union[datetime, None] = None
    status: Union[str, None] = None

    class Config:
        orm_mode = True


class AllUserBorrowHistoryResponse(BaseModel):
    id: Union[int, None] = Field(alias="id")
    book_name: Union[str, None] = None
    user_name: Union[str, None] = None
    ask_from_time: Union[datetime, None] = None
    ask_to_time: Union[datetime, None] = None
    alloted_from_time: Union[datetime, None] = None
    alloted_to_time: Union[datetime, None] = None
    status: Union[str, None] = None

    class Config:
        orm_mode = True
