from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from utils import *
from models import User
import crud
import database
from schemas import *


router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_dep = Annotated[str, Depends(oauth2_scheme)]


@router.post("/register")
async def create_new_user(user: SignupModel, db: database.Session = Depends(database.get_db)):
    db_user = crud.create_user(db, user)
    return db_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: database.Session = Depends(database.get_db)
    ) -> Token:
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    print("TOken user:", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={'sub': user.username}, expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")