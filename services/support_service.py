from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.support import Support
from repositories import support_repository, user_repository, work_repository


def support_work_service(
    db: Session,
    work_id: int,
    supporter_id: int,
    amount: Decimal,
) -> Support:
    work = work_repository.get_work_by_id(db, work_id)

    if work is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found",
        )

    return support_repository.create_support(
        db=db,
        work_id=work_id,
        supporter_id=supporter_id,
        amount=amount,
    )


def get_supports_for_work_service(
    db: Session,
    work_id: int,
) -> list[Support]:
    work = work_repository.get_work_by_id(db, work_id)

    if work is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found",
        )

    return support_repository.get_supports_by_work_id(
        db=db,
        work_id=work_id,
    )


def get_supports_for_user_service(
    db: Session,
    user_id: int,
) -> list[Support]:
    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return support_repository.get_supports_by_supporter_id(
        db=db,
        user_id=user_id,
    )


get_user_supports_service = get_supports_for_user_service
