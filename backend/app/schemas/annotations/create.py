from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class AnnotationCreate(BaseModel):
    labeling_task_id: int
    image_path: str
    class_id: int
    class_name: str
    bbox_x: Decimal = Field(ge=0, le=1)
    bbox_y: Decimal = Field(ge=0, le=1)
    bbox_width: Decimal = Field(ge=0, le=1)
    bbox_height: Decimal = Field(ge=0, le=1)
    confidence: Decimal | None = Field(default=None, ge=0, le=1)
    created_by: int | None = None


class AnnotationBulkCreate(BaseModel):
    items: List[AnnotationCreate]
