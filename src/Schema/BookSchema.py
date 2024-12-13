from pydantic import BaseModel
from typing import Union

class BookSchema(BaseModel):
    name: Union[str, None] = ""
    category: Union[str, None] = ""
    author_name: Union[str, None] = ""

    class Config:
        orm_mode = True
    
