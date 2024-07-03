import os
from datetime import datetime, timedelta, timezone
from typing import Union, Any, Annotated
from jose import jwt, JWTError
from jwt import InvalidTokenError
from passlib.context import CryptContext

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from schemas import User, UserInDB

from dotenv import load_dotenv
load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')
oauth2_dep = Annotated[str, Depends(oauth2_scheme)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        # "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "is_active": False,
    },
    "alice": {
        "username": "alice",
        # "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "is_active": True,
    },
}


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)



def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", is_active=fake_users_db.get(token).get('is_active')
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
    ):
    print("Current user:", current_user)
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)