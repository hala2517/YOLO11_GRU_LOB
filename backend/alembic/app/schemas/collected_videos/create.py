from datetime import datetime

from app.models.enums import CollectedVideoStatus
from pydantic import BaseModel, Field


class CollectedVideoCreate(BaseModel):
    camera_id: int
    site_id: int
    data_collection_job_id: int | None = None
    recognition_log_id: int | None = None
    file_path: str
    file_name: str
    file_size_bytes: int | None = Field(default=None, ge=0)
    duration_seconds: int | None = Field(default=None, ge=0)
    recorded_at: datetime
    start_time: datetime | None = None
    end_time: datetime | None = None
    resolution: str | None = None
    fps: int | None = Field(default=None, ge=1)
    storage_type: str = "local"
    status: CollectedVideoStatus = CollectedVideoStatus.pending
