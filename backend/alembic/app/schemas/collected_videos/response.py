from datetime import datetime
from typing import List

from app.models.enums import CollectedVideoStatus
from pydantic import BaseModel, ConfigDict


class CollectedVideoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    camera_id: int
    site_id: int
    data_collection_job_id: int | None = None
    recognition_log_id: int | None = None
    file_path: str
    file_name: str
    file_size_bytes: int | None = None
    duration_seconds: int | None = None
    recorded_at: datetime
    start_time: datetime | None = None
    end_time: datetime | None = None
    resolution: str | None = None
    fps: int | None = None
    storage_type: str
    status: CollectedVideoStatus
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class CollectedVideoListResponse(BaseModel):
    items: List[CollectedVideoResponse]
    total: int
    page: int
    size: int
