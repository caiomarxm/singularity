from typing import Callable, MutableMapping, Awaitable, Any, Optional
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from singularity.authentication.oauth2.token_manager import TokenManager
from singularity.authentication.rbac.permission_checker import PermissionChecker
from singularity.database.engine import get_session
from singularity.database.models.rbac import User
from singularity.server.middleware.rbac_permissions import ROUTE_PERMISSION_MAPPING


class RBACMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Callable[
            [
                MutableMapping[str, Any],
                Callable[[], Awaitable[MutableMapping[str, Any]]],
                Callable[[MutableMapping[str, Any]], Awaitable[None]],
            ],
            Awaitable[None],
        ],
    ) -> None:
        super().__init__(app)
        self.open_routes = ["/login", "/docs", "/openapi.json"]

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.url.path in self.open_routes:
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")

        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authorization header missing",
            )

        token = authorization.replace("Bearer ", "")

        try:
            session = next(get_session())

            user: Optional[User] = TokenManager.get_current_user(
                token=token, session=session
            )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token or user not found",
                )

            required_permission, level, entity_id = self.resolve_permission(request)

            if not PermissionChecker.user_has_permission(
                user, required_permission, level, entity_id
            ):
                raise HTTPException(status_code=403, detail="Permission denied")

            return await call_next(request)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Server error: {str(e)}",
            )

    def resolve_permission(self, request: Request):
        path = request.url.path.lstrip("/")
        method = request.method
        path_parts = path.split("/")

        permission_info = ROUTE_PERMISSION_MAPPING
        entity_id = None

        for path_part in path_parts:
            if path_part in permission_info:
                permission_info = permission_info[path_part]
            else:  # Dynamic part with {entity_id}
                entity_id = path_part
                entity = next(
                    filter(
                        lambda key: "{" in key and "}" in key,
                        permission_info.keys(),
                    )
                )
                permission_info = permission_info[entity]

        if (
            "permissions" in permission_info
            and method in permission_info["permissions"]
        ):
            required_permission = permission_info["permissions"][method]
            level = permission_info["level"]
            return required_permission, level, entity_id
        else:
            raise HTTPException(status_code=404, detail="Route not found")
