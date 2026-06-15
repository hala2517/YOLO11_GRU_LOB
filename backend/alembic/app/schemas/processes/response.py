from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class ProcessResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    site_id: int
    name: str
    code: str | None = None
    description: str | None = None
    line_order: int
    created_by: int | None = None
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class ProcessListResponse(BaseModel):
    items: List[ProcessResponse]
    total: int
    page: int
    size: int
