# built-in
from pydantic import BaseModel
from datetime import datetime


class BorrowRequestSchema(BaseModel):
    book_name: str
    ask_from_time: str
    ask_to_time: str

    class Config:
        orm_mode = True