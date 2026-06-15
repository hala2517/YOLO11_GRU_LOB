from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class WorkerDetectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recognition_log_id: int | None = None
    process_id: int | None = None
    site_id: int
    camera_id: int
    worker_label: str | None = None
    entry_time: datetime
    exit_time: datetime | None = None
    duration_seconds: int | None = None
    created_at: datetime


class WorkerDetectionListResponse(BaseModel):
    items: List[WorkerDetectionResponse]
    total: int
    page: int
    size: int
