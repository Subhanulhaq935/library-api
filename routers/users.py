from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from dependencies.auth import get_current_user
from models.user import User
from schemas.support import SupportResponse
from services import support_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }


@router.get(
    "/{user_id}/support",
    response_model=list[SupportResponse],
)
def get_user_supports(
    user_id: int,
    db: Session = Depends(get_db),
):
    return support_service.get_supports_for_user_service(
        db=db,
        user_id=user_id,
    )
