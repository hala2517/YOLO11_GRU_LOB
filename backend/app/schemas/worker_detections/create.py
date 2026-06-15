from datetime import datetime

from pydantic import BaseModel


class WorkerDetectionCreate(BaseModel):
    recognition_log_id: int | None = None
    process_id: int | None = None
    site_id: int
    camera_id: int
    worker_label: str | None = None
    entry_time: datetime
    exit_time: datetime | None = None
    duration_seconds: int | None = None
