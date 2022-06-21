from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

from lighthouse.ml_projects.db import UserRole


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None
    role: UserRole = UserRole.user


# properties to receive on user creation
class UserCreate(UserBase):
    email: EmailStr
    password: constr(min_length=8)
    first_name: constr(strip_whitespace=True, min_length=3)
    last_name: constr(strip_whitespace=True, min_length=3)


class UserInDBBase(UserBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# additional properties to be stored in DB
# but not exposed to the client
class UserInDB(UserInDBBase):
    hashed_password: str


# properties to return to the client
class User(UserInDBBase):
    ...
