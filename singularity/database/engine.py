import os
from typing import Generator
from sqlmodel import Session, create_engine

from singularity.settings.settings import settings


def create_sqlite_if_not_exists(settings):
    if settings.SINGULARITY_DB_TARGET == "sqlite":
        db_path = settings.SINGULARITY_DB_CONNECTION_URL.replace("sqlite:///", "")

        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        if not os.path.exists(db_path):
            open(db_path, "a").close()


DB_ENGINE = create_engine(
    settings.SINGULARITY_DB_CONNECTION_URL,
)


def get_session() -> Generator[Session, None, None]:
    with Session(DB_ENGINE) as session:
        yield session
