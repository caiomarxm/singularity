from typing import List, Optional
from sqlmodel import Session, select
from singularity.database.models.rbac import (
    Permission,
    PermissionCreate,
    PermissionUpdate,
)


def create_permission(session: Session, permission_in: PermissionCreate) -> Permission:
    statement = select(Permission).where(Permission.name == permission_in.name)
    db_permission = session.exec(statement=statement).first()

    if db_permission:
        raise ValueError(f"Permission with name {permission_in.name} already exists")

    db_permission = Permission(**permission_in.model_dump())
    session.add(db_permission)
    session.commit()
    session.refresh(db_permission)

    return db_permission


def read_permission(session: Session, permission_id: int) -> Optional[Permission]:
    return session.get(Permission, permission_id)


def read_permission_by_name(
    session: Session, permission_name: str
) -> Optional[Permission]:
    statement = select(Permission).where(Permission.name == permission_name)
    db_permission = session.exec(statement=statement).first()
    return db_permission


def update_permission(
    session: Session, permission_id: int, permission_update: PermissionUpdate
) -> Optional[Permission]:
    db_permission = session.get(Permission, permission_id)

    if not db_permission:
        return None

    for key, value in permission_update.model_dump().items():
        if value is not None:
            setattr(db_permission, key, value)

    session.commit()
    session.refresh(db_permission)

    return db_permission


def delete_permission(session: Session, permission_id: int) -> bool:
    db_permission = session.get(Permission, permission_id)

    if not db_permission:
        return False

    session.delete(db_permission)
    session.commit()

    return True


def list_permissions(
    session: Session, offset: int = 0, limit: int = 10
) -> List[Permission]:
    statement = select(Permission).offset(offset).limit(limit)
    permissions = session.exec(statement).all()
    return permissions
