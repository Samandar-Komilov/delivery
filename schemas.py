from pydantic import BaseModel
from typing import Optional


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

