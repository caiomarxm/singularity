from sqlmodel import Session

from singularity.database.models.rbac import (
    PermissionCreate,
    OrganizationCreate,
    OrganizationMembershipCreate,
    UserCreate,
    SquadCreate,
    SquadMembershipCreate,
    RoleCreate,
    RolePermissionCreate,
)
from singularity.database.repositories.rbac.user_repository import create_user
from singularity.database.repositories.rbac.permission_repository import (
    create_permission,
)
from singularity.database.repositories.rbac.role_repository import create_role
from singularity.database.repositories.rbac.role_permissions_repository import (
    create_role_permission,
)
from singularity.database.repositories.rbac.organization_repository import (
    create_organization,
)
from singularity.database.repositories.rbac.organization_memberships_repository import (
    create_organization_membership,
)
from singularity.database.repositories.rbac.squad_repository import create_squad
from singularity.database.repositories.rbac.squad_memberships_repository import (
    create_squad_membership,
)
from singularity.authentication.rbac.permission_checker import PermissionChecker


def create_rbac_test_data(session: Session):
    # Create permissions
    permission_view = create_permission(session, PermissionCreate(name="view"))
    permission_edit = create_permission(session, PermissionCreate(name="edit"))

    # Create roles
    role_admin = create_role(session, RoleCreate(name="admin"))
    role_org_admin = create_role(session, RoleCreate(name="org_admin"))
    role_squad_lead = create_role(session, RoleCreate(name="squad_lead"))

    # Assign permissions to roles
    create_role_permission(
        session,
        RolePermissionCreate(role_id=role_admin.id, permission_id=permission_view.id),
    )
    create_role_permission(
        session,
        RolePermissionCreate(role_id=role_admin.id, permission_id=permission_edit.id),
    )
    create_role_permission(
        session,
        RolePermissionCreate(
            role_id=role_org_admin.id, permission_id=permission_view.id
        ),
    )
    create_role_permission(
        session,
        RolePermissionCreate(
            role_id=role_squad_lead.id, permission_id=permission_edit.id
        ),
    )

    # Create users
    users = {
        "superadmin": create_user(
            session,
            UserCreate(
                email="admin@example.com",
                hashed_password="hash1234",
                is_superadmin=True,
            ),
        ),
        "org_admin": create_user(
            session,
            UserCreate(email="org_admin@example.com", hashed_password="hash1234"),
        ),
        "squad_lead": create_user(
            session,
            UserCreate(email="squad_lead@example.com", hashed_password="hash1234"),
        ),
        "no_permissions": create_user(
            session,
            UserCreate(email="no_permissions@example.com", hashed_password="hash1234"),
        ),
    }

    # Create organization and memberships
    organization = create_organization(
        session, OrganizationCreate(name="My Organization")
    )
    create_organization_membership(
        session,
        OrganizationMembershipCreate(
            user_id=users["org_admin"].id,
            organization_id=organization.id,
            role_id=role_org_admin.id,
        ),
    )

    # Create squad and memberships
    squad = create_squad(session, SquadCreate(name="My Squad"))
    create_squad_membership(
        session,
        SquadMembershipCreate(
            user_id=users["squad_lead"].id,
            squad_id=squad.id,
            role_id=role_squad_lead.id,
        ),
    )

    return users, organization.id, squad.id


def test_superadmin_has_all_permissions(session: Session):
    users, org_id, squad_id = create_rbac_test_data(session)
    superadmin = users["superadmin"]

    assert PermissionChecker.user_has_permission(
        superadmin, "view", "organization", org_id
    )
    assert PermissionChecker.user_has_permission(
        superadmin, "edit", "organization", org_id
    )
    assert PermissionChecker.user_has_permission(superadmin, "view", "squad", squad_id)
    assert PermissionChecker.user_has_permission(superadmin, "edit", "squad", squad_id)


def test_org_admin_has_org_permissions(session: Session):
    users, org_id, _ = create_rbac_test_data(session)
    org_admin = users["org_admin"]

    assert PermissionChecker.user_has_permission(
        org_admin, "view", "organization", org_id
    )
    assert not PermissionChecker.user_has_permission(
        org_admin, "edit", "organization", org_id
    )
    assert not PermissionChecker.user_has_permission(org_admin, "view", "squad", None)


def test_squad_lead_has_squad_permissions(session: Session):
    users, _, squad_id = create_rbac_test_data(session)
    squad_lead = users["squad_lead"]

    assert PermissionChecker.user_has_permission(squad_lead, "edit", "squad", squad_id)
    assert not PermissionChecker.user_has_permission(
        squad_lead, "view", "squad", squad_id
    )
    assert not PermissionChecker.user_has_permission(
        squad_lead, "view", "organization", None
    )


def test_user_with_no_permissions(session: Session):
    users, org_id, squad_id = create_rbac_test_data(session)
    no_permissions_user = users["no_permissions"]

    assert not PermissionChecker.user_has_permission(
        no_permissions_user, "view", "organization", org_id
    )
    assert not PermissionChecker.user_has_permission(
        no_permissions_user, "edit", "organization", org_id
    )
    assert not PermissionChecker.user_has_permission(
        no_permissions_user, "view", "squad", squad_id
    )
    assert not PermissionChecker.user_has_permission(
        no_permissions_user, "edit", "squad", squad_id
    )
