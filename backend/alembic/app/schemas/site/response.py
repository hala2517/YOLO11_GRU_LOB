from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict


class SiteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str | None = None
    description: str | None = None
    address: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    floor_plan_image_path: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class SiteListResponse(BaseModel):
    items: List[SiteResponse]
    total: int
    page: int
    size: int
