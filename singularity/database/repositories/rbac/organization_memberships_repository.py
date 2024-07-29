from typing import List, Optional
from sqlmodel import Session, select, and_
from singularity.database.models.rbac import (
    OrganizationMembership,
    OrganizationMembershipCreate,
)


def create_organization_membership(
    session: Session, membership_in: OrganizationMembershipCreate
) -> OrganizationMembership:
    statement = select(OrganizationMembership).where(
        and_(
            (OrganizationMembership.user_id == membership_in.user_id),
            (OrganizationMembership.organization_id == membership_in.organization_id),
        )
    )
    db_membership = session.exec(statement=statement).first()

    if db_membership:
        raise ValueError(
            f"Membership already exists for user {membership_in.user_id} in organization {membership_in.organization_id}"
        )

    db_membership = OrganizationMembership(**membership_in.model_dump())
    session.add(db_membership)
    session.commit()
    session.refresh(db_membership)

    return db_membership


def read_organization_membership(
    session: Session, user_id: int, organization_id: int
) -> Optional[OrganizationMembership]:
    return session.get(OrganizationMembership, (user_id, organization_id))


def update_organization_membership(
    session: Session,
    user_id: int,
    organization_id: int,
    role_id: int,
) -> Optional[OrganizationMembership]:
    db_membership = session.get(OrganizationMembership, (user_id, organization_id))

    if not db_membership:
        return None

    db_membership.role_id = role_id

    session.add(db_membership)
    session.commit()
    session.refresh(db_membership)

    return db_membership


def delete_organization_membership(
    session: Session, user_id: int, organization_id: int
) -> bool:
    db_membership = session.get(OrganizationMembership, (user_id, organization_id))

    if not db_membership:
        return False

    session.delete(db_membership)
    session.commit()

    return True


def list_organization_memberships(
    session: Session,
    offset: int = 0,
    limit: int = 10,
    organization_id: Optional[int] = None,
) -> List[OrganizationMembership]:
    statement = select(OrganizationMembership)

    if organization_id is not None:
        statement = statement.where(
            OrganizationMembership.organization_id == organization_id
        )

    statement = statement.offset(offset).limit(limit)
    memberships = session.exec(statement).all()
    return memberships
