from typing import List, Optional
from sqlmodel import Session, select, and_
from singularity.database.models.rbac import (
    RolePermission,
    RolePermissionCreate,
)


def create_role_permission(
    session: Session, role_permission_in: RolePermissionCreate
) -> RolePermission:
    statement = select(RolePermission).where(
        and_(
            (RolePermission.role_id == role_permission_in.role_id),
            (RolePermission.permission_id == role_permission_in.permission_id),
        )
    )
    db_role_permission = session.exec(statement=statement).first()

    if db_role_permission:
        raise ValueError(
            f"Permission {role_permission_in.permission_id} already assigned to role {role_permission_in.role_id}"
        )

    db_role_permission = RolePermission(**role_permission_in.model_dump())
    session.add(db_role_permission)
    session.commit()
    session.refresh(db_role_permission)

    return db_role_permission


def read_role_permission(
    session: Session, role_id: int, permission_id: int
) -> Optional[RolePermission]:
    return session.get(RolePermission, (role_id, permission_id))


def delete_role_permission(session: Session, role_id: int, permission_id: int) -> bool:
    db_role_permission = session.get(RolePermission, (role_id, permission_id))

    if not db_role_permission:
        return False

    session.delete(db_role_permission)
    session.commit()

    return True


def list_role_permissions(
    session: Session, offset: int = 0, limit: int = 10
) -> List[RolePermission]:
    statement = select(RolePermission).offset(offset).limit(limit)
    role_permissions = session.exec(statement).all()
    return role_permissions


def assign_permissions_to_role(
    session: Session, role_id: int, permission_ids: List[int]
) -> List[RolePermission]:
    # Query for existing permissions using the IN operator
    existing_permissions_query = select(RolePermission.permission_id).where(
        and_(
            RolePermission.role_id == role_id,
            RolePermission.permission_id.in_(permission_ids),
        )
    )
    existing_permissions = {
        permission_id
        for permission_id in session.exec(existing_permissions_query).all()
    }

    # Determine which permissions are not yet assigned
    new_permissions = [
        RolePermission(role_id=role_id, permission_id=permission_id)
        for permission_id in permission_ids
        if permission_id not in existing_permissions
    ]

    # Bulk add new permissions
    session.add_all(new_permissions)
    session.commit()

    return new_permissions
