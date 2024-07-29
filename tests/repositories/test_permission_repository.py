from singularity.database.models.rbac import PermissionCreate, PermissionUpdate
from singularity.database.repositories.rbac.permission_repository import (
    create_permission,
    read_permission,
    read_permission_by_name,
    update_permission,
    delete_permission,
    list_permissions,
)


def test_create_permission(session):
    permission_in = PermissionCreate(
        name="view_dashboard", description="Permission to view the dashboard"
    )
    permission = create_permission(session, permission_in)

    assert permission.id is not None
    assert permission.name == "view_dashboard"
    assert permission.description == "Permission to view the dashboard"


def test_read_permission(session):
    permission_in = PermissionCreate(
        name="view_dashboard", description="Permission to view the dashboard"
    )
    permission = create_permission(session, permission_in)

    fetched_permission = read_permission(session, permission.id)
    assert fetched_permission is not None
    assert fetched_permission.name == "view_dashboard"


def test_read_permission_by_name(session):
    permission_in = PermissionCreate(
        name="view_dashboard", description="Permission to view the dashboard"
    )
    create_permission(session, permission_in)

    fetched_permission = read_permission_by_name(session, "view_dashboard")
    assert fetched_permission is not None
    assert fetched_permission.name == "view_dashboard"


def test_update_permission(session):
    permission_in = PermissionCreate(
        name="view_dashboard", description="Permission to view the dashboard"
    )
    permission = create_permission(session, permission_in)

    permission_update = PermissionUpdate(description="Updated description")
    updated_permission = update_permission(session, permission.id, permission_update)

    assert updated_permission.description == "Updated description"


def test_delete_permission(session):
    permission_in = PermissionCreate(
        name="view_dashboard", description="Permission to view the dashboard"
    )
    permission = create_permission(session, permission_in)

    result = delete_permission(session, permission.id)
    assert result is True

    fetched_permission = read_permission(session, permission.id)
    assert fetched_permission is None


def test_list_permissions(session):
    permission1 = PermissionCreate(
        name="view_dashboard", description="Permission to view the dashboard"
    )
    permission2 = PermissionCreate(
        name="edit_profile", description="Permission to edit user profile"
    )
    create_permission(session, permission1)
    create_permission(session, permission2)

    permissions = list_permissions(session)
    assert len(permissions) == 2
