
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from schemas.user import UserResponse


class WorkCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    content: str


class WorkUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    content: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            raise ValueError("Title cannot be null")

        return value


class WorkResponse(BaseModel):
    id: int
    title: str
    description: str | None
    content: str
    artist_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkDetailResponse(WorkResponse):
    author: UserResponse
    total_support: Decimal


WorkDetailsResponse = WorkDetailResponse
