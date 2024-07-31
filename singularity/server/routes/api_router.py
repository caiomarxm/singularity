from fastapi import APIRouter

from singularity.server.modules.authentication import authentication_controller
from singularity.server.modules.rbac import rbac_controller

api_router = APIRouter(prefix="")

api_router.include_router(
    authentication_controller.router, prefix="/login", tags=["login"]
)

api_router.include_router(rbac_controller.router, prefix="/rbac", tags=["rbac"])
