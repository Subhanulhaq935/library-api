from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.work import Work
from repositories import work_repository


def create_work_service(
    db: Session,
    work_data: dict,
    current_user_id: int,
):
    work_data["artist_id"] = current_user_id
    return work_repository.create_work(db, work_data)


def get_work_service(db: Session, work_id: int):
    work = work_repository.get_work_by_id(db, work_id)

    if work is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found",
        )

    return work


def get_work_details_service(db: Session, work_id: int):
    result = work_repository.get_work_details_by_id(db, work_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found",
        )

    work = result[0]
    author = result[1]
    total_support = result[2]

    return {
        "id": work.id,
        "title": work.title,
        "description": work.description,
        "content": work.content,
        "artist_id": work.artist_id,
        "created_at": work.created_at,
        "updated_at": work.updated_at,
        "author": {
            "id": author.id,
            "username": author.username,
            "email": author.email,
        },
        "total_support": total_support,
    }


def get_all_works_service(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
):
    return work_repository.get_all_works(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit,
    )


def update_work_service(
    db: Session,
    work_id: int,
    update_data: dict,
    current_user_id: int,
):
    work = get_work_service(db, work_id)

    if work.artist_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this work",
        )

    return work_repository.update_work(db, work, update_data)


def delete_work_service(
    db: Session,
    work_id: int,
    current_user_id: int,
):
    work = get_work_service(db, work_id)

    if work.artist_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this work",
        )

    work_repository.delete_work(db, work)
