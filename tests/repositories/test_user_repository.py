from singularity.database.models.rbac import UserIn, UserUpdate
from singularity.database.repositories.rbac.user_repository import (
    create_user,
    read_user,
    read_user_from_email,
    update_user,
    delete_user,
    list_users,
)


def test_create_user(session):
    user_in = UserIn(
        username="testuser", email="test@example.com", hashed_password="hashedpassword"
    )
    user = create_user(session, user_in)

    assert user.id is not None
    assert user.email == "test@example.com"


def test_read_user(session):
    user_in = UserIn(
        username="testuser", email="test@example.com", hashed_password="hashedpassword"
    )
    user = create_user(session, user_in)

    fetched_user = read_user(session, user.id)
    assert fetched_user is not None
    assert fetched_user.email == "test@example.com"


def test_read_user_from_email(session):
    user_in = UserIn(
        username="testuser", email="test@example.com", hashed_password="hashedpassword"
    )
    create_user(session, user_in)

    fetched_user = read_user_from_email(session, "test@example.com")
    assert fetched_user is not None
    assert fetched_user.email == "test@example.com"


def test_update_user(session):
    user_in = UserIn(
        username="testuser", email="test@example.com", hashed_password="hashedpassword"
    )
    user = create_user(session, user_in)

    user_update = UserUpdate(email="updated@example.com")
    updated_user = update_user(session, user.id, user_update)

    assert updated_user.email == "updated@example.com"


def test_delete_user(session):
    user_in = UserIn(
        username="testuser", email="test@example.com", hashed_password="hashedpassword"
    )
    user = create_user(session, user_in)

    result = delete_user(session, user.id)
    assert result is True

    fetched_user = read_user(session, user.id)
    assert fetched_user is None


def test_list_users(session):
    user1 = UserIn(
        username="user1", email="user1@example.com", hashed_password="hashedpassword"
    )
    user2 = UserIn(
        username="user2", email="user2@example.com", hashed_password="hashedpassword"
    )
    create_user(session, user1)
    create_user(session, user2)

    users = list_users(session)
    assert len(users) == 2
