from datetime import datetime
from decimal import Decimal
from typing import Any, List

from app.models.enums import RecognitionType
from pydantic import BaseModel, ConfigDict


class RecognitionLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    site_id: int
    camera_id: int
    labeling_task_id: int | None = None
    recognition_type: RecognitionType
    class_name: str
    confidence: Decimal | None = None
    bbox: dict[str, Any] | None = None
    position_x: Decimal | None = None
    position_y: Decimal | None = None
    detected_at: datetime
    metadata_: dict[str, Any] | None = None
    created_at: datetime


class RecognitionLogListResponse(BaseModel):
    items: List[RecognitionLogResponse]
    total: int
    page: int
    size: int
