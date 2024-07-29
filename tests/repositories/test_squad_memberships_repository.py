from singularity.database.models.rbac import SquadMembershipCreate
from singularity.database.repositories.rbac.squad_memberships_repository import (
    create_squad_membership,
    read_squad_membership,
    update_squad_membership,
    delete_squad_membership,
    list_squad_memberships,
)


def test_create_squad_membership(session):
    membership_in = SquadMembershipCreate(user_id=1, squad_id=1, role_id=1)
    membership = create_squad_membership(session, membership_in)

    assert membership.user_id == 1
    assert membership.squad_id == 1
    assert membership.role_id == 1


def test_read_squad_membership(session):
    membership_in = SquadMembershipCreate(user_id=1, squad_id=1, role_id=1)
    create_squad_membership(session, membership_in)

    fetched_membership = read_squad_membership(session, 1, 1)
    assert fetched_membership is not None
    assert fetched_membership.user_id == 1
    assert fetched_membership.squad_id == 1
    assert fetched_membership.role_id == 1


def test_update_squad_membership(session):
    membership_in = SquadMembershipCreate(user_id=1, squad_id=1, role_id=1)
    create_squad_membership(session, membership_in)

    updated_membership = update_squad_membership(session, 1, 1, role_id=2)

    assert updated_membership is not None
    assert updated_membership.role_id == 2


def test_delete_squad_membership(session):
    membership_in = SquadMembershipCreate(user_id=1, squad_id=1, role_id=1)
    create_squad_membership(session, membership_in)

    result = delete_squad_membership(session, 1, 1)
    assert result is True

    fetched_membership = read_squad_membership(session, 1, 1)
    assert fetched_membership is None


def test_list_squad_memberships(session):
    membership1 = SquadMembershipCreate(user_id=1, squad_id=1, role_id=1)
    membership2 = SquadMembershipCreate(user_id=2, squad_id=1, role_id=2)
    create_squad_membership(session, membership1)
    create_squad_membership(session, membership2)

    memberships = list_squad_memberships(session)
    assert len(memberships) == 2

    memberships_with_filter = list_squad_memberships(session, squad_id=1)
    assert len(memberships_with_filter) == 2
