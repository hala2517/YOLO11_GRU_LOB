from decimal import Decimal

from pydantic import BaseModel, Field


class AnnotationUpdate(BaseModel):
    class_id: int | None = None
    class_name: str | None = None
    bbox_x: Decimal | None = Field(default=None, ge=0, le=1)
    bbox_y: Decimal | None = Field(default=None, ge=0, le=1)
    bbox_width: Decimal | None = Field(default=None, ge=0, le=1)
    bbox_height: Decimal | None = Field(default=None, ge=0, le=1)
    confidence: Decimal | None = Field(default=None, ge=0, le=1)
