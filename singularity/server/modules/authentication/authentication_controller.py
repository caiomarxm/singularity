from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from singularity.authentication.oauth2.token_manager import TokenManager
from singularity.authentication.security.password_manager import PasswordManager

from singularity.database.engine import get_session
from singularity.database.repositories.rbac.user_repository import read_user

from singularity.server.modules.authentication.authentication_schemas import (
    LoginResponseData,
)


router = APIRouter()


@router.post("", response_model=LoginResponseData)
def login_with_username_and_password(
    user_login: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = read_user(session=session, user_id=user_login.username)

    if not user or not PasswordManager.verify_password(
        user.hashed_password, user_login.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_encoded = TokenManager.create_access_token(
        sub=user.id, email=user.email
    )

    return access_token_encoded
