from fastapi import FastAPI

from singularity.server.lifespan import lifespan
from singularity.server.routes.api_router import api_router
from singularity.server.middleware.rbac_middleware import RBACMiddleware


app = FastAPI(lifespan=lifespan)

app.add_middleware(RBACMiddleware)

app.include_router(api_router)
