from typing import List, Optional
from sqlmodel import Session, select
from singularity.database.models.rbac import Tag, TagCreate, TagUpdate


def create_tag(session: Session, tag_in: TagCreate) -> Tag:
    statement = select(Tag).where(Tag.name == tag_in.name)
    db_tag = session.exec(statement=statement).first()

    if db_tag:
        raise ValueError(f"Tag with name {tag_in.name} already exists")

    db_tag = Tag(**tag_in.model_dump())
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)

    return db_tag


def read_tag(session: Session, tag_id: int) -> Optional[Tag]:
    return session.get(Tag, tag_id)


def read_tag_by_name(session: Session, tag_name: str) -> Optional[Tag]:
    statement = select(Tag).where(Tag.name == tag_name)
    db_tag = session.exec(statement=statement).first()
    return db_tag


def update_tag(session: Session, tag_id: int, tag_update: TagUpdate) -> Optional[Tag]:
    db_tag = session.get(Tag, tag_id)

    if not db_tag:
        return None

    for key, value in tag_update.model_dump().items():
        if value is not None:
            setattr(db_tag, key, value)

    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)

    return db_tag


def delete_tag(session: Session, tag_id: int) -> bool:
    db_tag = session.get(Tag, tag_id)

    if not db_tag:
        return False

    session.delete(db_tag)
    session.commit()

    return True


def list_tags(session: Session, offset: int = 0, limit: int = 10) -> List[Tag]:
    statement = select(Tag).offset(offset).limit(limit)
    tags = session.exec(statement).all()
    return tags
