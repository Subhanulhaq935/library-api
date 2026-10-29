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

