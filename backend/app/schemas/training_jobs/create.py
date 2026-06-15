from typing import Any

from pydantic import BaseModel


class TrainingJobCreate(BaseModel):
    job_name: str
    dataset_id: int
    model_id: int | None = None
    parameters: dict[str, Any] | None = None
    external_job_id: str | None = None
    source_system: str | None = None
    created_by: int | None = None
