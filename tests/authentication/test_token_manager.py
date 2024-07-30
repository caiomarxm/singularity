import pytest
from datetime import datetime, timedelta
from sqlmodel import Session

from singularity.settings.settings import settings

from singularity.authentication.oauth2.token_manager import TokenManager
from singularity.authentication.oauth2.models import (
    Oauth2AccessTokenContent,
    OAuth2AccessTokenEncoded,
)

from singularity.database.models.rbac import User, UserCreate
from singularity.database.repositories.rbac.user_repository import create_user


@pytest.fixture
def user(session: Session) -> User:
    user_create = UserCreate(
        email="testuser@example.com", hashed_password="testhashedpassword"
    )
    return create_user(session=session, user_in=user_create)


def test_create_access_token(user: User):
    data = Oauth2AccessTokenContent(sub=user.id, email=user.email, exp=datetime.now())
    token_manager = TokenManager()

    access_token_encoded = token_manager.create_access_token(
        data=data, expires_delta=timedelta(days=settings.JWT_EXPIRES_IN_DAYS)
    )

    assert isinstance(access_token_encoded, OAuth2AccessTokenEncoded)
    assert access_token_encoded.access_token is not None
    assert len(access_token_encoded.access_token) > 0


def test_verify_token(user: User):
    data = Oauth2AccessTokenContent(
        sub=user.id,
        email=user.email,
        exp=datetime.now() + timedelta(days=settings.JWT_EXPIRES_IN_DAYS),
    )

    access_token_encoded = TokenManager.create_access_token(data=data)
    token = access_token_encoded.access_token

    payload = TokenManager.verify_token(token)

    assert payload is not None
    assert isinstance(payload, Oauth2AccessTokenContent)
    assert payload.sub == str(user.id)
    assert payload.email == user.email


def test_get_current_user(session: Session, user: User):
    data = Oauth2AccessTokenContent(
        sub=user.id,
        email=user.email,
        exp=datetime.now() + timedelta(days=settings.JWT_EXPIRES_IN_DAYS),
    )
    token_manager = TokenManager()

    access_token_encoded = token_manager.create_access_token(data=data)
    token = access_token_encoded.access_token

    current_user = token_manager.get_current_user(token=token, session=session)

    assert current_user is not None
    assert isinstance(current_user, User)
    assert current_user.id == user.id
    assert current_user.email == user.email
