from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict


class AnnotationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    labeling_task_id: int
    image_path: str
    class_id: int
    class_name: str
    bbox_x: Decimal
    bbox_y: Decimal
    bbox_width: Decimal
    bbox_height: Decimal
    confidence: Decimal | None = None
    created_by: int | None = None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class AnnotationListResponse(BaseModel):
    items: List[AnnotationResponse]
    total: int
    page: int
    size: int


class LabelItem(BaseModel):
    label_id: int
    class_id: int
    class_name: str
    bbox: List[float]
    confidence: float | None = None


class ImageWithLabelsResponse(BaseModel):
    image_id: str
    image_url: str
    width: int | None = None
    height: int | None = None
    labels: List[LabelItem]
