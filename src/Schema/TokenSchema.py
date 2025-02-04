from pydantic import BaseModel
from typing import Any


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user: dict
