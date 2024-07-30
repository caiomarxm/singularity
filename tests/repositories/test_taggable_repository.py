from sqlmodel import Session
from singularity.database.models.rbac import TaggableCreate, TaggableUpdate
from singularity.database.repositories.rbac.taggable_repository import (
    create_taggable,
    read_taggable,
    update_taggable,
    delete_taggable,
    list_taggables,
)


def test_create_taggable(session: Session):
    taggable_in = TaggableCreate(tag_id=1, taggable_id=1, taggable_type="test_type")
    taggable = create_taggable(session, taggable_in)

    assert taggable.tag_id == 1
    assert taggable.taggable_id == 1
    assert taggable.taggable_type == "test_type"


def test_read_taggable(session: Session):
    taggable_in = TaggableCreate(tag_id=1, taggable_id=1, taggable_type="test_type")
    taggable = create_taggable(session, taggable_in)

    fetched_taggable = read_taggable(
        session, taggable.tag_id, taggable.taggable_id, taggable.taggable_type
    )
    assert fetched_taggable is not None
    assert fetched_taggable.tag_id == 1
    assert fetched_taggable.taggable_id == 1
    assert fetched_taggable.taggable_type == "test_type"


def test_update_taggable(session: Session):
    taggable_in = TaggableCreate(tag_id=1, taggable_id=1, taggable_type="test_type")
    taggable = create_taggable(session, taggable_in)

    taggable_update = TaggableUpdate(taggable_type="updated_type")
    updated_taggable = update_taggable(
        session,
        taggable.tag_id,
        taggable.taggable_id,
        taggable.taggable_type,
        taggable_update,
    )

    assert updated_taggable.taggable_type == "updated_type"


def test_delete_taggable(session: Session):
    taggable_in = TaggableCreate(tag_id=1, taggable_id=1, taggable_type="test_type")
    taggable = create_taggable(session, taggable_in)

    result = delete_taggable(
        session, taggable.tag_id, taggable.taggable_id, taggable.taggable_type
    )
    assert result is True

    fetched_taggable = read_taggable(
        session, taggable.tag_id, taggable.taggable_id, taggable.taggable_type
    )
    assert fetched_taggable is None


def test_list_taggables(session: Session):
    taggable1 = TaggableCreate(tag_id=1, taggable_id=1, taggable_type="type1")
    taggable2 = TaggableCreate(tag_id=2, taggable_id=2, taggable_type="type2")
    create_taggable(session, taggable1)
    create_taggable(session, taggable2)

    taggables = list_taggables(session)
    assert len(taggables) == 2
    assert taggables[0].taggable_type == "type1"
    assert taggables[1].taggable_type == "type2"
