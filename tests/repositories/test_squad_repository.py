from singularity.database.models.rbac import SquadCreate, SquadUpdate
from singularity.database.repositories.rbac.squad_repository import (
    create_squad,
    read_squad,
    read_squad_by_name,
    update_squad,
    delete_squad,
    list_squads,
)


def test_create_squad(session):
    squad_in = SquadCreate(name="Alpha Squad", description="First squad")
    squad = create_squad(session, squad_in)

    assert squad.id is not None
    assert squad.name == "Alpha Squad"
    assert squad.description == "First squad"


def test_read_squad(session):
    squad_in = SquadCreate(name="Alpha Squad", description="First squad")
    squad = create_squad(session, squad_in)

    fetched_squad = read_squad(session, squad.id)
    assert fetched_squad is not None
    assert fetched_squad.name == "Alpha Squad"


def test_read_squad_by_name(session):
    squad_in = SquadCreate(name="Alpha Squad", description="First squad")
    create_squad(session, squad_in)

    fetched_squad = read_squad_by_name(session, "Alpha Squad")
    assert fetched_squad is not None
    assert fetched_squad.name == "Alpha Squad"


def test_update_squad(session):
    squad_in = SquadCreate(name="Alpha Squad", description="First squad")
    squad = create_squad(session, squad_in)

    squad_update = SquadUpdate(description="Updated description")
    updated_squad = update_squad(session, squad.id, squad_update)

    assert updated_squad.description == "Updated description"


def test_delete_squad(session):
    squad_in = SquadCreate(name="Alpha Squad", description="First squad")
    squad = create_squad(session, squad_in)

    result = delete_squad(session, squad.id)
    assert result is True

    fetched_squad = read_squad(session, squad.id)
    assert fetched_squad is None


def test_list_squads(session):
    squad1 = SquadCreate(name="Alpha Squad", description="First squad")
    squad2 = SquadCreate(name="Beta Squad", description="Second squad")
    create_squad(session, squad1)
    create_squad(session, squad2)

    squads = list_squads(session)
    assert len(squads) == 2
    assert any(sq.name == "Alpha Squad" for sq in squads)
    assert any(sq.name == "Beta Squad" for sq in squads)
