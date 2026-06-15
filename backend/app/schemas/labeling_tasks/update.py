from datetime import datetime

from app.models.enums import LabelingTaskStatus
from pydantic import BaseModel, Field


class LabelingTaskUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: LabelingTaskStatus | None = None
    assigned_to: int | None = None
    progress: int | None = Field(default=None, ge=0, le=100)
    total_images: int | None = Field(default=None, ge=0)
    labeled_images: int | None = Field(default=None, ge=0)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    is_active: bool | None = None
