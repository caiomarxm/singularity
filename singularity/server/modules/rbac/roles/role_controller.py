from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status

from singularity.database.engine import get_session
from singularity.database.models.rbac import Role, RoleCreate, RoleUpdate, User
from singularity.database.repositories.rbac.role_repository import (
    create_role,
    read_role,
    update_role,
    delete_role,
    list_roles,
    count_total_roles,
)

from singularity.server.core.security_deps import get_current_user
from singularity.server.pagination.pagination_schema import (
    PaginatedResponse,
    PaginationMetadata,
)

router = APIRouter()


@router.post("/", response_model=Role, dependencies=[Depends(get_current_user)])
def create_custom_role(
    role_in: RoleCreate,
    session: Session = Depends(get_session),
):
    try:
        return create_role(session, role_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{role_id}", response_model=Role)
def get_role_by_id(
    role_id: int,
    session: Session = Depends(get_session),
):
    role = read_role(session, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return role


@router.get("/", response_model=PaginatedResponse[Role])
def list_roles_paginated(
    page: int = 1,
    per_page: int = 10,
    session: Session = Depends(get_session),
):
    offset = (page - 1) * per_page
    roles = list_roles(session, offset=offset, limit=per_page)
    roles_count = count_total_roles(session=session)

    return PaginatedResponse(
        data=roles,
        metadata=PaginationMetadata(
            page=page,
            per_page=per_page,
            total_count=roles_count,
        ),
    )


@router.put("/{role_id}", response_model=Role)
def update_role_by_id(
    role_id: int,
    role_update: RoleUpdate,
    session: Session = Depends(get_session),
):
    role = update_role(session, role_id, role_update)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return role


@router.delete("/{role_id}", response_model=Role)
def delete_role_by_id(
    role_id: int,
    session: Session = Depends(get_session),
):
    deleted = delete_role(session, role_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return {"detail": "Role deleted successfully"}
