from fastapi import APIRouter

from singularity.server.modules.rbac.roles import role_controller


router = APIRouter()

router.include_router(role_controller.router, prefix="/roles")
