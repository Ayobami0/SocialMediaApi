from datetime import timedelta
from typing_extensions import Annotated

from fastapi import (
    APIRouter, status,
    HTTPException, Depends)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.db import get_db
from .models.token import Token
from .jwt_handlers import (
    create_access_token, authenticate_user
)

ACCESS_TOKEN_EXPIRE_MINUTES = 20
auth_route = APIRouter()


@auth_route.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db,
                             form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email_address}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
