from pydantic import BaseModel
from lighthouse.ml_projects.db import UserRole


class TokenData(BaseModel):
    user_id: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email: str
    password: str
