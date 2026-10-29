from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SupportCreate(BaseModel):
    amount: Decimal = Field(gt=0)


class SupportResponse(BaseModel):
    id: int
    work_id: int
    supporter_id: int
    amount: Decimal
    supported_at: datetime

    model_config = ConfigDict(from_attributes=True)
