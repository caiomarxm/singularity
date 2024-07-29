from typing import List, Optional
from sqlmodel import Session, select

from singularity.database.models.rbac import (
    User,
    UserCreate,
    UserUpdate,
    SquadMembership,
    OrganizationMembership,
)


def create_user(session: Session, user_in: UserCreate) -> User:
    statement = select(User).where(User.email == user_in.email)
    db_user = session.exec(statement=statement).first()

    if db_user:
        raise ValueError(f"User with email {user_in.email} already exists")

    user_in = User(**user_in.model_dump())

    session.add(user_in)
    session.commit()
    session.refresh(user_in)

    return user_in


def read_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def read_user_from_email(session: Session, user_email: str) -> Optional[User]:
    statement = select(User).where(User.email == user_email)
    db_user = session.exec(statement=statement).first()
    return db_user


def update_user(
    session: Session, user_id: int, user_update: UserUpdate
) -> Optional[User]:
    db_user = session.get(User, user_id)

    if not db_user:
        return None

    for key, value in user_update.model_dump().items():
        if value is not None:
            setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def delete_user(session: Session, user_id: int) -> bool:
    db_user = session.get(User, user_id)

    if not db_user:
        return False

    session.delete(db_user)
    session.commit()

    return True


def list_users(
    session: Session,
    offset: int = 0,
    limit: int = 10,
    organization_id: Optional[int] = None,
    squad_id: Optional[int] = None,
) -> List[User]:
    statement = select(User)

    if organization_id:
        statement = statement.join(User.organization_memberships).where(
            OrganizationMembership.organization_id == organization_id
        )

    if squad_id:
        statement = statement.join(User.squad_memberships).where(
            SquadMembership.squad_id == squad_id
        )

    statement = statement.offset(offset).limit(limit)
    return session.exec(statement=statement).all()
