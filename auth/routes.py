import datetime
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_

from schemas import SignupModel, LoginModel
from database import engine, session
from models import User
from utils import Hasher, create_access_token, create_refresh_token


router = APIRouter(prefix="/auth")
session = session(bind=engine)


@router.get("/")
async def base_auth():
    return {"message": "Signup uchun"}


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignupModel):
    email = session.query(User).filter(User.email==user.email).first()
    if email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already exists.")
    username = session.query(User).filter(User.username==user.username).first()
    if username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username already exists.")
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        is_active = user.is_active,
        is_staff = user.is_staff
    )

    session.add(new_user)
    session.commit()

    data = {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'is_staff': new_user.is_staff,
        'is_active': new_user.is_active
    }
    response_model = {
        'success': True,
        'code': 201,
        'message': "User is created successfully",
        'data': data
    }

    return response_model


@router.post('/login', status_code=200)
async def login(form_data: LoginModel = Depends()):
    db_user = session.query(User).filter(
        or_(
            User.username == form_data.username_or_email,
            User.email == form_data.username_or_email
        )
    ).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or username')
    
    hashed_pass = db_user.password
    if not Hasher.verify_password(form_data.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    token = {
        "access": create_access_token(db_user.username),
        "refresh": create_refresh_token(db_user.username)
    }

    response = {
        "success": True,
        "code": 200,
        "message": "User successfully logged in!",
        "data": token
    }

    return response