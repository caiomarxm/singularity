from typing import List, Optional
from sqlmodel import Session, select, and_
from singularity.database.models.rbac import (
    SquadMembership,
    SquadMembershipCreate,
)


def create_squad_membership(
    session: Session, membership_in: SquadMembershipCreate
) -> SquadMembership:
    statement = select(SquadMembership).where(
        and_(
            (SquadMembership.user_id == membership_in.user_id),
            (SquadMembership.squad_id == membership_in.squad_id),
        )
    )
    db_membership = session.exec(statement=statement).first()

    if db_membership:
        raise ValueError(
            f"Membership already exists for user {membership_in.user_id} in squad {membership_in.squad_id}"
        )

    db_membership = SquadMembership(**membership_in.model_dump())
    session.add(db_membership)
    session.commit()
    session.refresh(db_membership)

    return db_membership


def read_squad_membership(
    session: Session, user_id: int, squad_id: int
) -> Optional[SquadMembership]:
    return session.get(SquadMembership, (user_id, squad_id))


def update_squad_membership(
    session: Session,
    user_id: int,
    squad_id: int,
    role_id: Optional[int],
) -> Optional[SquadMembership]:
    db_membership = session.get(SquadMembership, (user_id, squad_id))

    if not db_membership:
        return None

    db_membership.role_id = role_id

    session.add(db_membership)
    session.commit()
    session.refresh(db_membership)

    return db_membership


def delete_squad_membership(session: Session, user_id: int, squad_id: int) -> bool:
    db_membership = session.get(SquadMembership, (user_id, squad_id))

    if not db_membership:
        return False

    session.delete(db_membership)
    session.commit()

    return True


def list_squad_memberships(
    session: Session,
    offset: int = 0,
    limit: int = 10,
    squad_id: Optional[int] = None,
) -> List[SquadMembership]:
    statement = select(SquadMembership)

    if squad_id is not None:
        statement = statement.where(SquadMembership.squad_id == squad_id)

    statement = statement.offset(offset).limit(limit)
    memberships = session.exec(statement).all()
    return memberships
