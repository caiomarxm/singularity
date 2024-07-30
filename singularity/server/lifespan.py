from contextlib import asynccontextmanager

from fastapi import FastAPI

from singularity.database.engine import get_session
from singularity.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = next(get_session())
    init_db(session=session)

    # Check services sucha as Redis, RabbitMQ ...

    yield
