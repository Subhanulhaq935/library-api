
from sqlalchemy.orm import Session
from models.work import Work


def create_work(db: Session, work_data: dict) -> Work:
    new_work = Work(**work_data)

    db.add(new_work)
    db.commit()
    db.refresh(new_work)

    return new_work


def get_work_by_id(db: Session, work_id: int):
    return (
        db.query(Work)
        .filter(Work.id == work_id)
        .first()
    )


def get_all_works(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
):
    query = db.query(Work)

    if author_id is not None:
        query = query.filter(Work.artist_id == author_id)

    return query.offset(skip).limit(limit).all()


def update_work(db: Session, work: Work, update_data: dict) -> Work:
    for field, value in update_data.items():
        setattr(work, field, value)

    db.commit()
    db.refresh(work)

    return work


def delete_work(db: Session, work: Work) -> None:
    db.delete(work)
    db.commit()
