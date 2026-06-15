from datetime import datetime
from typing import Any

from app.models.enums import TrainingJobStatus
from pydantic import BaseModel


class TrainingJobUpdate(BaseModel):
    job_name: str | None = None
    model_id: int | None = None
    status: TrainingJobStatus | None = None
    parameters: dict[str, Any] | None = None
    metrics: dict[str, Any] | None = None
    progress: int | None = None
    external_job_id: str | None = None
    source_system: str | None = None
    raw_events: list[dict[str, Any]] | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
