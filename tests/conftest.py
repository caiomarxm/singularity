import pytest

from singularity.database.models.rbac import *

from sqlmodel import SQLModel, Session, create_engine


from singularity.database.models.rbac import User, UserCreate
from singularity.database.repositories.rbac.user_repository import create_user

FIXTURE_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def user(session: Session) -> User:
    user_create = UserCreate(
        email="testuser@example.com", hashed_password="testhashedpassword"
    )
    return create_user(session=session, user_in=user_create)
