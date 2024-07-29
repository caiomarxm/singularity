from typing import List, Optional
from sqlmodel import Session, select
from singularity.database.models.rbac import (
    Organization,
    OrganizationCreate,
    OrganizationUpdate,
)


def create_organization(
    session: Session, organization_in: OrganizationCreate
) -> Organization:
    statement = select(Organization).where(Organization.name == organization_in.name)
    db_organization = session.exec(statement=statement).first()

    if db_organization:
        raise ValueError(
            f"Organization with name {organization_in.name} already exists"
        )

    db_organization = Organization(**organization_in.model_dump())
    session.add(db_organization)
    session.commit()
    session.refresh(db_organization)

    return db_organization


def read_organization(session: Session, organization_id: int) -> Optional[Organization]:
    return session.get(Organization, organization_id)


def read_organization_by_name(
    session: Session, organization_name: str
) -> Optional[Organization]:
    statement = select(Organization).where(Organization.name == organization_name)
    db_organization = session.exec(statement=statement).first()
    return db_organization


def update_organization(
    session: Session, organization_id: int, organization_update: OrganizationUpdate
) -> Optional[Organization]:
    db_organization = session.get(Organization, organization_id)

    if not db_organization:
        return None

    for key, value in organization_update.model_dump().items():
        if value is not None:
            setattr(db_organization, key, value)

    session.commit()
    session.refresh(db_organization)

    return db_organization


def delete_organization(session: Session, organization_id: int) -> bool:
    db_organization = session.get(Organization, organization_id)

    if not db_organization:
        return False

    session.delete(db_organization)
    session.commit()

    return True


def list_organizations(
    session: Session, offset: int = 0, limit: int = 10
) -> List[Organization]:
    statement = select(Organization).offset(offset).limit(limit)
    organizations = session.exec(statement).all()
    return organizations
