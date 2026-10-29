from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from core.database import get_db
from dependencies.auth import get_current_user
from models.user import User
from schemas.support import SupportCreate, SupportResponse
from schemas.work import WorkCreate, WorkUpdate, WorkResponse, WorkDetailResponse
from services import support_service, work_service

router = APIRouter(prefix="/works", tags=["Works"])


@router.post("/", response_model=WorkResponse, status_code=201)
def create_work(
    work_data: WorkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return work_service.create_work_service(
        db=db,
        work_data=work_data.model_dump(),
        current_user_id=current_user.id,
    )


@router.get("/", response_model=list[WorkResponse])
def get_all_works(
    author_id: int | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return work_service.get_all_works_service(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{work_id}", response_model=WorkResponse)
def get_work(
    work_id: int,
    db: Session = Depends(get_db),
):
    return work_service.get_work_service(db, work_id)


@router.get(
    "/{work_id}/details",
    response_model=WorkDetailResponse,
)
def get_work_details(
    work_id: int,
    db: Session = Depends(get_db),
):
    return work_service.get_work_details_service(db, work_id)


@router.put("/{work_id}", response_model=WorkResponse)
def update_work(
    work_id: int,
    work_data: WorkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    update_data = work_data.model_dump(exclude_unset=True)

    return work_service.update_work_service(
        db=db,
        work_id=work_id,
        update_data=update_data,
        current_user_id=current_user.id,
    )


@router.delete("/{work_id}", status_code=204)
def delete_work(
    work_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    work_service.delete_work_service(
        db=db,
        work_id=work_id,
        current_user_id=current_user.id,
    )


@router.post(
    "/{work_id}/support",
    response_model=SupportResponse,
    status_code=status.HTTP_201_CREATED,
)
def support_work(
    work_id: int,
    support_data: SupportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return support_service.support_work_service(
        db=db,
        work_id=work_id,
        supporter_id=current_user.id,
        amount=support_data.amount,
    )


@router.get(
    "/{work_id}/support",
    response_model=list[SupportResponse],
)
def get_supports_for_work(
    work_id: int,
    db: Session = Depends(get_db),
):
    return support_service.get_supports_for_work_service(
        db=db,
        work_id=work_id,
    )
