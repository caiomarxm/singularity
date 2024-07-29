from typing import List, Optional
from sqlmodel import Session, select
from singularity.database.models.rbac import Squad, SquadCreate, SquadUpdate


def create_squad(session: Session, squad_in: SquadCreate) -> Squad:
    statement = select(Squad).where(Squad.name == squad_in.name)
    db_squad = session.exec(statement=statement).first()

    if db_squad:
        raise ValueError(f"Squad with name {squad_in.name} already exists")

    db_squad = Squad(**squad_in.model_dump())
    session.add(db_squad)
    session.commit()
    session.refresh(db_squad)

    return db_squad


def read_squad(session: Session, squad_id: int) -> Optional[Squad]:
    return session.get(Squad, squad_id)


def read_squad_by_name(session: Session, squad_name: str) -> Optional[Squad]:
    statement = select(Squad).where(Squad.name == squad_name)
    db_squad = session.exec(statement=statement).first()
    return db_squad


def update_squad(
    session: Session, squad_id: int, squad_update: SquadUpdate
) -> Optional[Squad]:
    db_squad = session.get(Squad, squad_id)

    if not db_squad:
        return None

    for key, value in squad_update.model_dump().items():
        if value is not None:
            setattr(db_squad, key, value)

    session.add(db_squad)
    session.commit()
    session.refresh(db_squad)

    return db_squad


def delete_squad(session: Session, squad_id: int) -> bool:
    db_squad = session.get(Squad, squad_id)

    if not db_squad:
        return False

    session.delete(db_squad)
    session.commit()

    return True


def list_squads(session: Session, offset: int = 0, limit: int = 10) -> List[Squad]:
    statement = select(Squad).offset(offset).limit(limit)
    squads = session.exec(statement).all()
    return squads
