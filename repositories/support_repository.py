from decimal import Decimal
from sqlalchemy.orm import Session

from models.support import Support


def create_support(
    db: Session,
    work_id: int,
    supporter_id: int,
    amount: Decimal,
) -> Support:
    new_support = Support(
        work_id=work_id,
        supporter_id=supporter_id,
        amount=amount,
    )

    db.add(new_support)
    db.commit()
    db.refresh(new_support)

    return new_support


def get_supports_by_work_id(db: Session, work_id: int) -> list[Support]:
    return (
        db.query(Support)
        .filter(Support.work_id == work_id)
        .all()
    )


def get_supports_by_supporter_id(db: Session, user_id: int) -> list[Support]:
    return (
        db.query(Support)
        .filter(Support.supporter_id == user_id)
        .all()
    )


def get_supports_by_user_id(db: Session, user_id: int) -> list[Support]:
    return get_supports_by_supporter_id(db, user_id)
