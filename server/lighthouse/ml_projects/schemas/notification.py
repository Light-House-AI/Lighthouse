from datetime import datetime
from pydantic import BaseModel, constr


class Notification(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    title: constr(min_length=3)
    body: constr(min_length=3)

    class Config:
        orm_mode = True