from fastapi import FastAPI

from singularity.server.lifespan import lifespan
from singularity.server.routes.api_router import api_router


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
