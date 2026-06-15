from datetime import datetime
from decimal import Decimal
from typing import List

from app.models.enums import AIModelType
from pydantic import BaseModel, ConfigDict


class AIModelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    version: str
    model_type: AIModelType
    description: str | None = None
    file_path: str | None = None
    file_size_bytes: int | None = None
    mAP: Decimal | None = None
    precision: Decimal | None = None
    recall: Decimal | None = None
    is_active: bool
    is_deployed: bool
    trained_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AIModelListResponse(BaseModel):
    items: List[AIModelResponse]
    total: int
    page: int
    size: int
