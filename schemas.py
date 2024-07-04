from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    email: str | None = None
    is_active: bool | None = None

class UserInDB(User):
    password: str


class SignupModel(BaseModel):
    username: str
    email: str
    password: str


class LoginModel(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None