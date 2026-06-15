from app.models.enums import DataCollectionJobStatus
from pydantic import BaseModel


class DataCollectionJobCreate(BaseModel):
    camera_id: int
    dataset_id: int | None = None
    job_name: str
    status: DataCollectionJobStatus = DataCollectionJobStatus.pending
    schedule_cron: str | None = None
    interval_minutes: int | None = None
    created_by: int | None = None
    is_active: bool = True
