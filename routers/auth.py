
from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.user import UserCreate, UserResponse, Token
from services.auth_service import (
    register_user_service,
    login_user_service,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user_service(db, user_data)



@router.post("/login", response_model=Token)
def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    return login_user_service(
        db=db,
        email=email,
        password=password,
    )

@router.post("/token", response_model=Token)
def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    return login_user_service(
        db=db,
        email=username,
        password=password,
    )

