import pytest
from singularity.database.models.rbac import (
    Role,
    Permission,
    RolePermissionCreate,
)
from singularity.database.repositories.rbac.role_permissions_repository import (
    create_role_permission,
    read_role_permission,
    delete_role_permission,
    list_role_permissions,
    assign_permissions_to_role,
)


@pytest.fixture
def setup_data(session):
    role = Role(name="Admin Role")
    permission1 = Permission(name="Read", description="Read permission")
    permission2 = Permission(name="Write", description="Write permission")

    session.add(role)
    session.add(permission1)
    session.add(permission2)
    session.commit()

    return role, permission1, permission2


def test_create_role_permission(session, setup_data):
    role, permission1, _ = setup_data

    role_permission_in = RolePermissionCreate(
        role_id=role.id, permission_id=permission1.id
    )
    role_permission = create_role_permission(session, role_permission_in)

    assert role_permission.role_id == role.id
    assert role_permission.permission_id == permission1.id


def test_read_role_permission(session, setup_data):
    role, permission1, _ = setup_data

    role_permission_in = RolePermissionCreate(
        role_id=role.id, permission_id=permission1.id
    )
    create_role_permission(session, role_permission_in)

    fetched_role_permission = read_role_permission(session, role.id, permission1.id)
    assert fetched_role_permission is not None
    assert fetched_role_permission.role_id == role.id
    assert fetched_role_permission.permission_id == permission1.id


def test_delete_role_permission(session, setup_data):
    role, permission1, _ = setup_data

    role_permission_in = RolePermissionCreate(
        role_id=role.id, permission_id=permission1.id
    )
    create_role_permission(session, role_permission_in)

    result = delete_role_permission(session, role.id, permission1.id)
    assert result is True

    fetched_role_permission = read_role_permission(session, role.id, permission1.id)
    assert fetched_role_permission is None


def test_list_role_permissions(session, setup_data):
    role, permission1, permission2 = setup_data

    create_role_permission(
        session, RolePermissionCreate(role_id=role.id, permission_id=permission1.id)
    )
    create_role_permission(
        session, RolePermissionCreate(role_id=role.id, permission_id=permission2.id)
    )

    role_permissions = list_role_permissions(session)
    assert len(role_permissions) == 2


def test_assign_permissions_to_role(session, setup_data):
    role, permission1, permission2 = setup_data

    permissions = assign_permissions_to_role(
        session, role.id, [permission1.id, permission2.id]
    )

    assert len(permissions) == 2
    assert all(p.role_id == role.id for p in permissions)
    assert all(p.permission_id in [permission1.id, permission2.id] for p in permissions)

    # Ensure no duplicate entries
    permissions = assign_permissions_to_role(
        session, role.id, [permission1.id, permission2.id]
    )
    assert len(permissions) == 0
