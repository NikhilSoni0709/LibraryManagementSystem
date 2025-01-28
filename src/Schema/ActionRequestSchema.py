from pydantic import BaseModel


class ActionRequestSchema(BaseModel):
    action: str
    borrow_id: int