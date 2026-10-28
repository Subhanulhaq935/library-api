
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkCreate(BaseModel):
    title: str
    description: str | None = None
    content: str


class WorkUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    content: str | None = None


class WorkResponse(BaseModel):
    id: int
    title: str
    description: str | None
    content: str
    artist_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
