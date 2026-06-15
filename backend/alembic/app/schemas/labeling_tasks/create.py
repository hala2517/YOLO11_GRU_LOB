from app.models.enums import LabelingTaskStatus
from pydantic import BaseModel, Field


class LabelingTaskCreate(BaseModel):
    dataset_id: int
    name: str
    description: str | None = None
    status: LabelingTaskStatus = LabelingTaskStatus.pending
    assigned_to: int | None = None
    total_images: int = Field(default=0, ge=0)
    created_by: int | None = None
    is_active: bool = True
