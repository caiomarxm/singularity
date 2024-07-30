from typing import List, Optional
from sqlmodel import Session, select, and_
from singularity.database.models.rbac import (
    Taggable,
    TaggableCreate,
    TaggableUpdate,
)


def create_taggable(session: Session, taggable_in: TaggableCreate) -> Taggable:
    statement = select(Taggable).where(
        and_(
            (Taggable.tag_id == taggable_in.tag_id),
            (Taggable.taggable_id == taggable_in.taggable_id),
            (Taggable.taggable_type == taggable_in.taggable_type),
        )
    )
    db_taggable = session.exec(statement=statement).first()

    if db_taggable:
        raise ValueError(
            f"Taggable already exists with tag_id {taggable_in.tag_id}, "
            f"taggable_id {taggable_in.taggable_id}, and taggable_type {taggable_in.taggable_type}"
        )

    db_taggable = Taggable(**taggable_in.model_dump())
    session.add(db_taggable)
    session.commit()
    session.refresh(db_taggable)

    return db_taggable


def read_taggable(
    session: Session, tag_id: int, taggable_id: int, taggable_type: str
) -> Optional[Taggable]:
    return session.get(Taggable, (tag_id, taggable_id, taggable_type))


def update_taggable(
    session: Session,
    tag_id: int,
    taggable_id: int,
    taggable_type: str,
    taggable_update: TaggableUpdate,
) -> Optional[Taggable]:
    db_taggable = session.get(Taggable, (tag_id, taggable_id, taggable_type))

    if not db_taggable:
        return None

    for key, value in taggable_update.model_dump().items():
        if value is not None:
            setattr(db_taggable, key, value)

    session.add(db_taggable)
    session.commit()
    session.refresh(db_taggable)

    return db_taggable


def delete_taggable(
    session: Session, tag_id: int, taggable_id: int, taggable_type: str
) -> bool:
    db_taggable = session.get(Taggable, (tag_id, taggable_id, taggable_type))

    if not db_taggable:
        return False

    session.delete(db_taggable)
    session.commit()

    return True


def list_taggables(
    session: Session, tag_id: Optional[int] = None, offset: int = 0, limit: int = 10
) -> List[Taggable]:
    statement = select(Taggable).offset(offset).limit(limit)

    if tag_id:
        statement = statement.where(Taggable.tag_id == tag_id)

    taggables = session.exec(statement).all()
    return taggables
