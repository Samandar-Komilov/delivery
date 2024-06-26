from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from schemas import SignupModel
from database import engine, session
from models import User
from hasher import Hasher


router = APIRouter(prefix="/auth")
session = session(bind=engine)


@router.get("/")
async def signup():
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
    return new_user