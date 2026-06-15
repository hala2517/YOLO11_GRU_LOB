from datetime import datetime

from pydantic import BaseModel


class WorkerDetectionUpdate(BaseModel):
    process_id: int | None = None
    worker_label: str | None = None
    exit_time: datetime | None = None
    duration_seconds: int | None = None
