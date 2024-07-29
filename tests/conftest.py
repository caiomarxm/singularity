import pytest

from singularity.database.models.rbac import *

from sqlmodel import SQLModel, Session, create_engine


FIXTURE_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session
