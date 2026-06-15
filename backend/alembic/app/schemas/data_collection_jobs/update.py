from datetime import datetime

from app.models.enums import DataCollectionJobStatus
from pydantic import BaseModel


class DataCollectionJobUpdate(BaseModel):
    dataset_id: int | None = None
    job_name: str | None = None
    status: DataCollectionJobStatus | None = None
    schedule_cron: str | None = None
    interval_minutes: int | None = None
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    total_captured: int | None = None
    error_message: str | None = None
    is_active: bool | None = None
