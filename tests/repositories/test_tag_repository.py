from sqlmodel import Session
from singularity.database.models.rbac import TagCreate, TagUpdate
from singularity.database.repositories.rbac.tag_repository import (
    create_tag,
    read_tag,
    read_tag_by_name,
    update_tag,
    delete_tag,
    list_tags,
)


def test_create_tag(session: Session):
    tag_in = TagCreate(name="test_tag", description="Test Description")
    tag = create_tag(session, tag_in)

    assert tag.id is not None
    assert tag.name == "test_tag"
    assert tag.description == "Test Description"


def test_read_tag(session: Session):
    tag_in = TagCreate(name="test_tag", description="Test Description")
    tag = create_tag(session, tag_in)

    fetched_tag = read_tag(session, tag.id)
    assert fetched_tag is not None
    assert fetched_tag.name == "test_tag"
    assert fetched_tag.description == "Test Description"


def test_read_tag_by_name(session: Session):
    tag_in = TagCreate(name="test_tag", description="Test Description")
    create_tag(session, tag_in)

    fetched_tag = read_tag_by_name(session, "test_tag")
    assert fetched_tag is not None
    assert fetched_tag.name == "test_tag"
    assert fetched_tag.description == "Test Description"


def test_update_tag(session: Session):
    tag_in = TagCreate(name="test_tag", description="Test Description")
    tag = create_tag(session, tag_in)

    tag_update = TagUpdate(description="Updated Description")
    updated_tag = update_tag(session, tag.id, tag_update)

    assert updated_tag.description == "Updated Description"


def test_delete_tag(session: Session):
    tag_in = TagCreate(name="test_tag", description="Test Description")
    tag = create_tag(session, tag_in)

    result = delete_tag(session, tag.id)
    assert result is True

    fetched_tag = read_tag(session, tag.id)
    assert fetched_tag is None


def test_list_tags(session: Session):
    tag1 = TagCreate(name="tag1", description="Description 1")
    tag2 = TagCreate(name="tag2", description="Description 2")
    create_tag(session, tag1)
    create_tag(session, tag2)

    tags = list_tags(session)
    assert len(tags) == 2
    assert tags[0].name == "tag1"
    assert tags[1].name == "tag2"
