# built-in
import re
from pydantic import BaseModel, model_validator
from typing import Union


class UserSchema(BaseModel):
    name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    category: Union[str, None] = None

    class Config:
        orm_mode = True

    # @model_validator(mode="before")
    # @classmethod
    # def validate_email(cls, field_values):
    #     email = field_values["email"]
    #     valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    #     assert valid, f"Invalid email."
    #     return field_values
