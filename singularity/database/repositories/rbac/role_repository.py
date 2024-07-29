from typing import List, Optional
from sqlmodel import Session, select
from singularity.database.models.rbac import Role, RoleCreate, RoleUpdate


def create_role(session: Session, role_in: RoleCreate) -> Role:
    statement = select(Role).where(Role.name == role_in.name)
    db_role = session.exec(statement=statement).first()

    if db_role:
        raise ValueError(f"Role with name {role_in.name} already exists")

    db_role = Role(**role_in.model_dump())
    session.add(db_role)
    session.commit()
    session.refresh(db_role)

    return db_role


def read_role(session: Session, role_id: int) -> Optional[Role]:
    return session.get(Role, role_id)


def read_role_by_name(session: Session, role_name: str) -> Optional[Role]:
    statement = select(Role).where(Role.name == role_name)
    db_role = session.exec(statement=statement).first()
    return db_role


def update_role(
    session: Session, role_id: int, role_update: RoleUpdate
) -> Optional[Role]:
    db_role = session.get(Role, role_id)

    if not db_role:
        return None

    for key, value in role_update.model_dump().items():
        if value is not None:
            setattr(db_role, key, value)

    session.commit()
    session.refresh(db_role)

    return db_role


def delete_role(session: Session, role_id: int) -> bool:
    db_role = session.get(Role, role_id)

    if not db_role:
        return False

    session.delete(db_role)
    session.commit()

    return True


def list_roles(session: Session, offset: int = 0, limit: int = 10) -> List[Role]:
    statement = select(Role).offset(offset).limit(limit)
    roles = session.exec(statement).all()
    return roles
