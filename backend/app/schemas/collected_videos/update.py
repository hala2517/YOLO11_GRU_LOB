from datetime import datetime

from app.models.enums import CollectedVideoStatus
from pydantic import BaseModel, Field


class CollectedVideoUpdate(BaseModel):
    file_size_bytes: int | None = Field(default=None, ge=0)
    duration_seconds: int | None = Field(default=None, ge=0)
    start_time: datetime | None = None
    end_time: datetime | None = None
    resolution: str | None = None
    fps: int | None = Field(default=None, ge=1)
    storage_type: str | None = None
    status: CollectedVideoStatus | None = None
    recognition_log_id: int | None = None
    data_collection_job_id: int | None = None
