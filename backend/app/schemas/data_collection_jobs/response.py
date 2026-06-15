from datetime import datetime
from typing import List

from app.models.enums import DataCollectionJobStatus
from pydantic import BaseModel, ConfigDict


class DataCollectionJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    camera_id: int
    dataset_id: int | None = None
    job_name: str
    status: DataCollectionJobStatus
    schedule_cron: str | None = None
    interval_minutes: int | None = None
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    total_captured: int
    error_message: str | None = None
    created_by: int | None = None
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class DataCollectionJobListResponse(BaseModel):
    items: List[DataCollectionJobResponse]
    total: int
    page: int
    size: int
