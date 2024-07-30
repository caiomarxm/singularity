from contextlib import asynccontextmanager

from sqlmodel import Session
from fastapi import FastAPI, Depends

from singularity.database.engine import get_session
from singularity.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = next(get_session())
    init_db(session=session)

    # Check services sucha as Redis, RabbitMQ ...

    yield
