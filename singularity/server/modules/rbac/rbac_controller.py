from fastapi import APIRouter

from singularity.server.modules.rbac.roles import role_controller
from singularity.server.modules.rbac.permissions import permission_controller


router = APIRouter()

router.include_router(role_controller.router, prefix="/roles")
router.include_router(permission_controller.router, prefix="/permissions")
