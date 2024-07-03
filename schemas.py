from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    email: str | None = None
    # fullname: str | None = None
    is_active: bool | None = None

class UserInDB(User):
    hashed_password: str


class SignupModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]


class LoginModel(BaseModel):
    username_or_email: str
    password: str

