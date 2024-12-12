# built-in
from pydantic import BaseModel
from typing import Union
from datetime import datetime

from src.Schema.BookSchema import BookSchema

class UserBorrowHistoryResponse(BaseModel):
    book: Union[BookSchema, None] = None
    from_time: Union[datetime, None] = None
    to_time: Union[datetime, None] = None
    status: Union[str, None] = None
