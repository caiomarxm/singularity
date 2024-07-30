from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from sqlmodel import Session

from singularity.authentication.security.password_manager import PasswordManager

from singularity.server.modules.authentication.authentication_schemas import (
    LoginRequestData,
)
from singularity.server.modules.authentication.authentication_controller import (
    login_with_username_and_password,
)
from singularity.database.models.rbac import User, UserCreate
from singularity.database.repositories.rbac.user_repository import (
    create_user,
)
from singularity.server.server import app


client = TestClient(app)


def test_login_success(session: Session):
    # Create user directly in the test function
    password = "testpassword"
    user_data = {
        "email": "testuser@example.com",
        "hashed_password": PasswordManager.hash_password(password, rounds=4),
        "name": "Test User",
    }

    db_user = create_user(session=session, user_in=UserCreate(**user_data))

    login_data = {"username": db_user.email, "password": password}

    response = login_with_username_and_password(
        user_login=OAuth2PasswordRequestForm(
            username=login_data["username"], password=login_data["password"]
        ),
        session=session,
    )

    assert response is not None
    assert "access_token" in response.model_dump()
    assert response.token_type == "bearer"


def test_login_failure_invalid_password(
    session: Session, user_with_hashed_password: User
):
    login_data = LoginRequestData(
        username="testuser@example.com", password="wrongpassword"
    )
    response = client.post("/login", data=login_data.model_dump())

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_failure_user_not_found(session: Session):
    login_data = LoginRequestData(
        username="nonexistentuser@example.com", password="somepassword"
    )
    response = client.post("/login", data=login_data.model_dump())

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
