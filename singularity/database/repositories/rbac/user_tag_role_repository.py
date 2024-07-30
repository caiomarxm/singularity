from typing import List, Optional
from sqlmodel import Session, select, and_
from singularity.database.models.rbac import (
    UserTagRole,
    UserTagRoleCreate,
)


def create_user_tag_role(
    session: Session, user_tag_role_in: UserTagRoleCreate
) -> UserTagRole:
    statement = select(UserTagRole).where(
        and_(
            (UserTagRole.user_id == user_tag_role_in.user_id),
            (UserTagRole.tag_id == user_tag_role_in.tag_id),
        )
    )
    db_user_tag_role = session.exec(statement=statement).first()

    if db_user_tag_role:
        raise ValueError(
            f"UserTagRole already exists for user {user_tag_role_in.user_id} with tag {user_tag_role_in.tag_id}"
        )

    db_user_tag_role = UserTagRole(**user_tag_role_in.model_dump())
    session.add(db_user_tag_role)
    session.commit()
    session.refresh(db_user_tag_role)

    return db_user_tag_role


def read_user_tag_role(
    session: Session, user_id: int, tag_id: int
) -> Optional[UserTagRole]:
    return session.get(UserTagRole, (user_id, tag_id))


def update_user_tag_role(
    session: Session, user_id: int, tag_id: int, role_id: int
) -> Optional[UserTagRole]:
    db_user_tag_role = session.get(UserTagRole, (user_id, tag_id))

    if not db_user_tag_role:
        return None

    db_user_tag_role.role_id = role_id

    session.add(db_user_tag_role)
    session.commit()
    session.refresh(db_user_tag_role)

    return db_user_tag_role


def delete_user_tag_role(session: Session, user_id: int, tag_id: int) -> bool:
    db_user_tag_role = session.get(UserTagRole, (user_id, tag_id))

    if not db_user_tag_role:
        return False

    session.delete(db_user_tag_role)
    session.commit()

    return True


def list_user_tag_roles(
    session: Session, offset: int = 0, limit: int = 10, tag_id: Optional[int] = None
) -> List[UserTagRole]:
    statement = select(UserTagRole)

    if tag_id is not None:
        statement = statement.where(UserTagRole.tag_id == tag_id)

    statement = statement.offset(offset).limit(limit)
    user_tag_roles = session.exec(statement).all()
    return user_tag_roles
