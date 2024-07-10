from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from models import User, Order
from database import get_db, session, engine
from schemas import UserInDB, LoginModel, TokenData, OrderModel
from utils import *


def get_user(session: Session, username: str):
    return session.query(User).filter(User.username == username).first()


def authenticate_user(session: Session, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token)
    user = get_user(session, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_admin_user(user: User = Depends(get_current_user)):
    if user.is_staff == True:
        return user
    else:
        credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": "Bearer"},
    )
        raise credentials_exception


def create_user(session: Session, user: LoginModel):
    existing_user = session.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    user_count = session.query(User).count()
    is_staff = user_count == 0

    db_user = User(
        username=user.username,
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_staff=is_staff
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user