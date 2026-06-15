from datetime import datetime
from decimal import Decimal
from typing import Any, List

from app.models.enums import RecognitionType
from pydantic import BaseModel, Field


class RecognitionLogCreate(BaseModel):
    site_id: int
    camera_id: int
    labeling_task_id: int | None = None
    recognition_type: RecognitionType
    class_name: str
    confidence: Decimal | None = Field(default=None, ge=0, le=1)
    bbox: dict[str, Any] | None = None
    position_x: Decimal | None = None
    position_y: Decimal | None = None
    detected_at: datetime
    metadata_: dict[str, Any] | None = None


class RecognitionLogBulkCreate(BaseModel):
    items: List[RecognitionLogCreate]
