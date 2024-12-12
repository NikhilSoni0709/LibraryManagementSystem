# built-in
from pydantic import BaseModel
from datetime import datetime


class BorrowRequestSchema(BaseModel):
    book_id: str
    from_time: str
    to_time: str

    class Config:
        orm_mode = True