from singularity.database.models.rbac import (
    UserCreate,
    RoleCreate,
    OrganizationCreate,
    OrganizationMembershipCreate,
)
from singularity.database.repositories.rbac.organization_memberships_repository import (
    create_organization_membership,
    read_organization_membership,
    update_organization_membership,
    delete_organization_membership,
    list_organization_memberships,
)
from singularity.database.repositories.rbac.user_repository import create_user
from singularity.database.repositories.rbac.role_repository import create_role
from singularity.database.repositories.rbac.organization_repository import (
    create_organization,
)


def test_create_organization_membership(session):
    # Setup required data
    user_in = UserCreate(
        username="testuser", email="test@example.com", hashed_password="hashedpassword"
    )
    role_in = RoleCreate(name="admin", description="Administrator role")
    organization_in = OrganizationCreate(name="Test Organization")

    user = create_user(session, user_in)
    role = create_role(session, role_in)
    organization = create_organization(session, organization_in)

    membership_in = OrganizationMembershipCreate(
        user_id=user.id, organization_id=organization.id, role_id=role.id
    )
    membership = create_organization_membership(session, membership_in)

    assert membership.user_id == user.id
    assert membership.organization_id == organization.id
    assert membership.role_id == role.id


def test_read_organization_membership(session):
    # Setup required data
    user_in = UserCreate(
        username="testuser", email="test@example.com", hashed_password="hashedpassword"
    )
    role_in = RoleCreate(name="admin", description="Administrator role")
    organization_in = OrganizationCreate(name="Test Organization")

    user = create_user(session, user_in)
    role = create_role(session, role_in)
    organization = create_organization(session, organization_in)

    membership_in = OrganizationMembershipCreate(
        user_id=user.id, organization_id=organization.id, role_id=role.id
    )
    create_organization_membership(session, membership_in)

    fetched_membership = read_organization_membership(session, user.id, organization.id)
    assert fetched_membership is not None
    assert fetched_membership.user_id == user.id
    assert fetched_membership.organization_id == organization.id


def test_update_organization_membership_role_id(session):
    # Setup required data
    user_in = UserCreate(
        username="testuser", email="test@example.com", hashed_password="hashedpassword"
    )
    role_in = RoleCreate(name="admin", description="Administrator role")
    updated_role_in = RoleCreate(name="user", description="User role")
    organization_in = OrganizationCreate(name="Test Organization")

    user = create_user(session, user_in)
    role = create_role(session, role_in)
    updated_role = create_role(session, updated_role_in)
    organization = create_organization(session, organization_in)

    membership_in = OrganizationMembershipCreate(
        user_id=user.id, organization_id=organization.id, role_id=role.id
    )
    create_organization_membership(session, membership_in)

    updated_membership = update_organization_membership(
        session, user.id, organization.id, updated_role.id
    )

    assert updated_membership is not None
    assert updated_membership.role_id == updated_role.id


def test_delete_organization_membership(session):
    # Setup required data
    user_in = UserCreate(
        username="testuser", email="test@example.com", hashed_password="hashedpassword"
    )
    role_in = RoleCreate(name="admin", description="Administrator role")
    organization_in = OrganizationCreate(name="Test Organization")

    user = create_user(session, user_in)
    role = create_role(session, role_in)
    organization = create_organization(session, organization_in)

    membership_in = OrganizationMembershipCreate(
        user_id=user.id, organization_id=organization.id, role_id=role.id
    )
    create_organization_membership(session, membership_in)

    result = delete_organization_membership(session, user.id, organization.id)
    assert result is True

    fetched_membership = read_organization_membership(session, user.id, organization.id)
    assert fetched_membership is None


def test_list_organization_memberships(session):
    # Setup required data
    user_in = UserCreate(
        username="testuser1",
        email="test1@example.com",
        hashed_password="hashedpassword",
    )
    user2_in = UserCreate(
        username="testuser2",
        email="test2@example.com",
        hashed_password="hashedpassword",
    )
    role_in = RoleCreate(name="admin", description="Administrator role")
    organization_in = OrganizationCreate(name="Test Organization")

    user1 = create_user(session, user_in)
    user2 = create_user(session, user2_in)
    role = create_role(session, role_in)
    organization = create_organization(session, organization_in)

    membership_in1 = OrganizationMembershipCreate(
        user_id=user1.id, organization_id=organization.id, role_id=role.id
    )
    membership_in2 = OrganizationMembershipCreate(
        user_id=user2.id, organization_id=organization.id, role_id=role.id
    )
    create_organization_membership(session, membership_in1)
    create_organization_membership(session, membership_in2)

    memberships = list_organization_memberships(
        session, organization_id=organization.id
    )
    assert len(memberships) == 2
    assert all(m.organization_id == organization.id for m in memberships)
