from datetime import datetime
from typing import List

from app.models.enums import LabelingTaskStatus
from pydantic import BaseModel, ConfigDict


class LabelingTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_id: int
    name: str
    description: str | None = None
    status: LabelingTaskStatus
    assigned_to: int | None = None
    progress: int
    total_images: int
    labeled_images: int
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_by: int | None = None
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class LabelingTaskListResponse(BaseModel):
    items: List[LabelingTaskResponse]
    total: int
    page: int
    size: int
