from sqlmodel import Session
from singularity.database.models.rbac import UserTagRoleCreate, UserTagRoleUpdate
from singularity.database.repositories.rbac.user_tag_role_repository import (
    create_user_tag_role,
    read_user_tag_role,
    update_user_tag_role,
    delete_user_tag_role,
    list_user_tag_roles,
)


def test_create_user_tag_role(session: Session):
    user_tag_role_in = UserTagRoleCreate(user_id=1, tag_id=1, role_id=1)
    user_tag_role = create_user_tag_role(session, user_tag_role_in)

    assert user_tag_role.user_id == 1
    assert user_tag_role.tag_id == 1
    assert user_tag_role.role_id == 1


def test_read_user_tag_role(session: Session):
    user_tag_role_in = UserTagRoleCreate(user_id=1, tag_id=1, role_id=1)
    user_tag_role = create_user_tag_role(session, user_tag_role_in)

    fetched_user_tag_role = read_user_tag_role(
        session, user_tag_role.user_id, user_tag_role.tag_id
    )
    assert fetched_user_tag_role is not None
    assert fetched_user_tag_role.user_id == 1
    assert fetched_user_tag_role.tag_id == 1
    assert fetched_user_tag_role.role_id == 1


def test_update_user_tag_role(session: Session):
    user_tag_role_in = UserTagRoleCreate(user_id=1, tag_id=1, role_id=1)
    user_tag_role = create_user_tag_role(session, user_tag_role_in)

    user_tag_role_update = UserTagRoleUpdate(role_id=2)
    updated_user_tag_role = update_user_tag_role(
        session,
        user_tag_role.user_id,
        user_tag_role.tag_id,
        user_tag_role_update.role_id,
    )

    assert updated_user_tag_role.role_id == 2


def test_delete_user_tag_role(session: Session):
    user_tag_role_in = UserTagRoleCreate(user_id=1, tag_id=1, role_id=1)
    user_tag_role = create_user_tag_role(session, user_tag_role_in)

    result = delete_user_tag_role(session, user_tag_role.user_id, user_tag_role.tag_id)
    assert result is True

    fetched_user_tag_role = read_user_tag_role(
        session, user_tag_role.user_id, user_tag_role.tag_id
    )
    assert fetched_user_tag_role is None


def test_list_user_tag_roles(session: Session):
    user_tag_role1 = UserTagRoleCreate(user_id=1, tag_id=1, role_id=1)
    user_tag_role2 = UserTagRoleCreate(user_id=2, tag_id=1, role_id=2)
    create_user_tag_role(session, user_tag_role1)
    create_user_tag_role(session, user_tag_role2)

    user_tag_roles = list_user_tag_roles(session, tag_id=1)
    assert len(user_tag_roles) == 2
    assert user_tag_roles[0].role_id == 1
    assert user_tag_roles[1].role_id == 2
