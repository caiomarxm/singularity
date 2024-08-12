from contextlib import asynccontextmanager

from fastapi import FastAPI

from singularity.database.engine import get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # session = next(get_session())

    # Check services such as Redis, RabbitMQ ...

    yield
