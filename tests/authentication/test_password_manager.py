from sqlmodel import Session

from singularity.database.models.rbac import UserCreate
from singularity.database.repositories.rbac.user_repository import create_user
from singularity.authentication.security.password_manager import PasswordManager


def test_password_hashing():
    password = "testpassword"
    hashed_password = PasswordManager.hash_password(password, rounds=4)
    assert isinstance(hashed_password, str)
    assert hashed_password != password


def test_password_verification(session: Session):
    password = "testpassword"
    hashed_password = PasswordManager.hash_password(password, rounds=4)

    user_create = UserCreate(
        email="verificationtestuser@example.com", hashed_password=hashed_password
    )
    user = create_user(session=session, user_in=user_create)

    stored_hashed_password = user.hashed_password

    correct_password = "testpassword"
    incorrect_password = "wrongpassword"

    assert PasswordManager.verify_password(stored_hashed_password, correct_password)
    assert not PasswordManager.verify_password(
        stored_hashed_password, incorrect_password
    )


def test_password_rehashing(session: Session):
    password = "newpassword"
    hashed_password = PasswordManager.hash_password(password, rounds=4)

    user_create = UserCreate(
        email="newuser@example.com", hashed_password=hashed_password
    )
    user = create_user(session=session, user_in=user_create)

    stored_hashed_password = user.hashed_password

    assert PasswordManager.verify_password(stored_hashed_password, password)

    rehashed_password = PasswordManager.hash_password(password, rounds=4)

    assert rehashed_password != stored_hashed_password

    assert PasswordManager.verify_password(rehashed_password, password)
