from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    user_id: int
    role: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email: EmailStr
    password: str
