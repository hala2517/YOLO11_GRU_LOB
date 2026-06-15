from datetime import datetime
from typing import Any, List

from app.models.enums import TrainingJobStatus
from pydantic import BaseModel, ConfigDict


class TrainingJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_name: str
    model_id: int | None = None
    dataset_id: int
    status: TrainingJobStatus
    parameters: dict[str, Any] | None = None
    metrics: dict[str, Any] | None = None
    progress: int
    external_job_id: str | None = None
    source_system: str | None = None
    raw_events: list[dict[str, Any]] | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    created_by: int | None = None
    created_at: datetime
    updated_at: datetime


class TrainingJobListResponse(BaseModel):
    items: List[TrainingJobResponse]
    total: int
    page: int
    size: int
