import logging
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlmodel import Session

from singularity.settings.settings import settings
from singularity.database.models.rbac import User
from singularity.authentication.oauth2.models import (
    Oauth2AccessTokenContent,
    OAuth2AccessTokenEncoded,
)
from singularity.database.repositories.rbac.user_repository import read_user


class TokenManager:
    @staticmethod
    def create_access_token(
        sub: int, email: str, expires_delta: Optional[timedelta] = None
    ) -> OAuth2AccessTokenEncoded:
        if expires_delta:
            expire = datetime.now() + expires_delta

        else:
            expire = datetime.now() + timedelta(days=settings.JWT_EXPIRES_IN_DAYS)

        to_encode = Oauth2AccessTokenContent(sub=str(sub), email=email, exp=expire)

        encoded_jwt = jwt.encode(
            to_encode.model_dump(),
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        return OAuth2AccessTokenEncoded(access_token=encoded_jwt)

    @staticmethod
    def verify_token(token: str) -> Optional[Oauth2AccessTokenContent]:
        try:
            payload = Oauth2AccessTokenContent(
                **jwt.decode(
                    token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
                )
            )
            if payload.sub is None or payload.email is None:
                return None

        except JWTError as err:
            logging.error(f"JWT Error: {err}")
            raise

        return payload

    @staticmethod
    def get_current_user(token: str, session: Session) -> Optional[User]:
        token_data = TokenManager.verify_token(token)

        if token_data:
            return read_user(session=session, user_id=token_data.sub)

        return None
