from typing import Any

from app.models.enums import MesSyncStatus
from pydantic import BaseModel


class MesSyncLogCreate(BaseModel):
    site_id: int
    payload: dict[str, Any]
    processed_status: MesSyncStatus = MesSyncStatus.pending
