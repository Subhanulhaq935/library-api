from sqlalchemy import func
from sqlalchemy.orm import Session

from models.support import Support
from models.user import User
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


def get_work_details_by_id(db: Session, work_id: int):
    return (
        db.query(
            Work,
            User,
            func.coalesce(func.sum(Support.amount), 0).label("total_support"),
        )
        .join(User, Work.artist_id == User.id)
        .outerjoin(Support, Work.id == Support.work_id)
        .filter(Work.id == work_id)
        .group_by(Work.id, User.id)
        .first()
    )


def get_all_works(
    db: Session,
    author_id: int | None = None,
    min_support: float | None = None,
    skip: int = 0,
    limit: int = 10,
):
    query = (
        db.query(
            Work,
            func.coalesce(func.sum(Support.amount), 0).label("total_support"),
        )
        .outerjoin(Support, Work.id == Support.work_id)
        .group_by(Work.id)
    )

    if author_id is not None:
        query = query.filter(Work.artist_id == author_id)

    if min_support is not None:
        query = query.having(
            func.coalesce(func.sum(Support.amount), 0) >= min_support
        )

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
