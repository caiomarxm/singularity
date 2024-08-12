from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status

from singularity.database.engine import get_session
from singularity.database.models.rbac import Permission
from singularity.database.repositories.rbac.permission_repository import (
    read_permission,
    list_permissions,
    count_total_permissions,
)

from singularity.server.pagination.pagination_schema import (
    PaginatedResponse,
    PaginationMetadata,
)

router = APIRouter()


@router.get("/{permission_id}", response_model=Permission)
def get_role_by_id(
    permission_id: int,
    session: Session = Depends(get_session),
):
    permission = read_permission(session, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    return permission


@router.get("/", response_model=PaginatedResponse[Permission])
def list_permissions_paginated(
    page: int = 1,
    per_page: int = 10,
    session: Session = Depends(get_session),
):
    offset = (page - 1) * per_page
    roles = list_permissions(session, offset=offset, limit=per_page)
    roles_count = count_total_permissions(session=session)

    return PaginatedResponse(
        data=roles,
        metadata=PaginationMetadata(
            page=page,
            per_page=per_page,
            total_count=roles_count,
        ),
    )
