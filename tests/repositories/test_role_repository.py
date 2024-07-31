from singularity.database.models.rbac import RoleCreate, RoleUpdate
from singularity.database.repositories.rbac.role_repository import (
    create_role,
    read_role,
    read_role_by_name,
    update_role,
    delete_role,
    list_roles,
    count_total_roles,
)


def test_create_role(session):
    role_in = RoleCreate(name="Admin", description="Administrator role")
    role = create_role(session, role_in)

    assert role.id is not None
    assert role.name == "Admin"
    assert role.description == "Administrator role"


def test_read_role(session):
    role_in = RoleCreate(name="Admin", description="Administrator role")
    role = create_role(session, role_in)

    fetched_role = read_role(session, role.id)
    assert fetched_role is not None
    assert fetched_role.name == "Admin"


def test_read_role_by_name(session):
    role_in = RoleCreate(name="Admin", description="Administrator role")
    create_role(session, role_in)

    fetched_role = read_role_by_name(session, "Admin")
    assert fetched_role is not None
    assert fetched_role.name == "Admin"


def test_update_role(session):
    role_in = RoleCreate(name="Admin", description="Administrator role")
    role = create_role(session, role_in)

    role_update = RoleUpdate(description="Updated description")
    updated_role = update_role(session, role.id, role_update)

    assert updated_role.description == "Updated description"


def test_delete_role(session):
    role_in = RoleCreate(name="Admin", description="Administrator role")
    role = create_role(session, role_in)

    result = delete_role(session, role.id)
    assert result is True

    fetched_role = read_role(session, role.id)
    assert fetched_role is None


def test_list_roles(session):
    role1 = RoleCreate(name="Admin", description="Administrator role")
    role2 = RoleCreate(name="User", description="Regular user role")
    create_role(session, role1)
    create_role(session, role2)

    roles = list_roles(session)
    assert len(roles) == 2


def test_count_roles(session):
    role1 = RoleCreate(name="Admin", description="Administrator role")
    role2 = RoleCreate(name="User", description="Regular user role")
    create_role(session, role1)
    create_role(session, role2)

    total_roles = count_total_roles(session=session)
    assert total_roles == 2
