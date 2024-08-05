from typing import Callable, MutableMapping, Awaitable, Any, Optional
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from singularity.authentication.oauth2.token_manager import TokenManager
from singularity.authentication.rbac.permission_checker import PermissionChecker
from singularity.database.engine import get_session
from singularity.database.models.rbac import User
from singularity.server.middleware.rbac.rbac_permissions_mapping import (
    RBAC_ROUTE_PERMISSION_MAPPING,
)


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
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Authorization header missing"},
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
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Permission denied"},
                )

            return await call_next(request)

        except HTTPException:
            raise

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": f"Server error: {str(e)}"},
            )

    def resolve_permission(self, request: Request):
        """
        Resolve the required permission, level, and entity_id based on the request path and method.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            Tuple[str, str, Optional[str]]: The required permission, level, and optional entity_id.
        """

        path = request.url.path.lstrip("/")
        method = request.method
        path_parts = path.split("/")

        permission_info = RBAC_ROUTE_PERMISSION_MAPPING
        entity_id = None

        for path_part in path_parts:
            if path_part in permission_info:
                permission_info = permission_info[path_part]
            elif path_part != "":  # Dynamic part with {entity_id}
                entity_id = path_part
                entity = next(
                    filter(
                        lambda key: "{" in key and "}" in key,
                        permission_info.keys(),
                    )
                )
                permission_info = permission_info[entity]

        # Last check to access the permissions if path doesn't end with a "/"
        if "" in permission_info.keys():
            permission_info = permission_info[""]

        if (
            "permissions" in permission_info
            and method in permission_info["permissions"]
        ):
            required_permission = permission_info["permissions"][method]
            level = permission_info["level"]
            return required_permission, level, entity_id
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "Route not found"},
            )
