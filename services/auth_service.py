
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from repositories.user_repository import (
    get_user_by_email,
    get_user_by_username,
    create_user,
)


def register_user_service(db: Session, user_data):
    existing_email = get_user_by_email(db, user_data.email)

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    existing_username = get_user_by_username(
        db,
        user_data.username,
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken",
        )

    password_hash = hash_password(user_data.password)

    return create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
    )


def login_user_service(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
