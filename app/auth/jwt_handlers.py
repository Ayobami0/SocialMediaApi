from typing import Union, Dict

from datetime import datetime, timedelta
from typing_extensions import Annotated

from jose import jwt, JWTError
from decouple import config

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from database.db import get_db
from database.crud.read import ReadRepository
from .models.token import TokenData


JWT_SECRET = config("SECRET")
JWT_ALGORITHM = config("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, email_address: str, password: str):
    user = ReadRepository.get_users_by_email(db, email_address)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: Dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=20)
    to_encode.update({'exp': expires})
    encoded_JWT = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_JWT


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email_address: str = payload.get("sub")
        if email_address is None:
            raise credentials_exception
        token_data = TokenData(email_address=email_address)
    except JWTError:
        raise credentials_exception
    user = ReadRepository.get_users_by_email(
        db=db,
        email_address=token_data.email_address)
    if user is None:
        raise credentials_exception
    return user
