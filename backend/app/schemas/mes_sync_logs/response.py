from datetime import datetime
from typing import Any, List

from app.models.enums import MesSyncStatus
from pydantic import BaseModel, ConfigDict


class MesSyncLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    site_id: int
    payload: dict[str, Any]
    processed_status: MesSyncStatus
    processed_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime


class MesSyncLogListResponse(BaseModel):
    items: List[MesSyncLogResponse]
    total: int
    page: int
    size: int
