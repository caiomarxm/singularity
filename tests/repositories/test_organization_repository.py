from singularity.database.models.rbac import OrganizationCreate, OrganizationUpdate
from singularity.database.repositories.rbac.organization_repository import (
    create_organization,
    read_organization,
    read_organization_by_name,
    update_organization,
    delete_organization,
    list_organizations,
)


def test_create_organization(session):
    organization_in = OrganizationCreate(name="Acme Corp")
    organization = create_organization(session, organization_in)

    assert organization.id is not None
    assert organization.name == "Acme Corp"


def test_read_organization(session):
    organization_in = OrganizationCreate(name="Acme Corp")
    organization = create_organization(session, organization_in)

    fetched_organization = read_organization(session, organization.id)
    assert fetched_organization is not None
    assert fetched_organization.name == "Acme Corp"


def test_read_organization_by_name(session):
    organization_in = OrganizationCreate(name="Acme Corp")
    create_organization(session, organization_in)

    fetched_organization = read_organization_by_name(session, "Acme Corp")
    assert fetched_organization is not None
    assert fetched_organization.name == "Acme Corp"


def test_update_organization(session):
    organization_in = OrganizationCreate(name="Acme Corp")
    organization = create_organization(session, organization_in)

    organization_update = OrganizationUpdate(name="Acme Corporation")
    updated_organization = update_organization(
        session, organization.id, organization_update
    )

    assert updated_organization.name == "Acme Corporation"


def test_delete_organization(session):
    organization_in = OrganizationCreate(name="Acme Corp")
    organization = create_organization(session, organization_in)

    result = delete_organization(session, organization.id)
    assert result is True

    fetched_organization = read_organization(session, organization.id)
    assert fetched_organization is None


def test_list_organizations(session):
    organization1 = OrganizationCreate(name="Acme Corp")
    organization2 = OrganizationCreate(name="Globex Corporation")
    create_organization(session, organization1)
    create_organization(session, organization2)

    organizations = list_organizations(session)
    assert len(organizations) == 2
    assert any(org.name == "Acme Corp" for org in organizations)
    assert any(org.name == "Globex Corporation" for org in organizations)
