from datetime import datetime
from decimal import Decimal
from typing import Any, List

from app.models.enums import AlertSeverity, AlertType
from pydantic import BaseModel, ConfigDict


class AlertThresholdResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    site_id: int
    alert_type: AlertType
    name: str
    description: str | None = None
    threshold_value: Decimal | None = None
    threshold_unit: str | None = None
    color_value: str | None = None
    conditions: dict[str, Any] | None = None
    is_active: bool
    created_by: int | None = None
    created_at: datetime
    updated_at: datetime


class AlertThresholdListResponse(BaseModel):
    items: List[AlertThresholdResponse]
    total: int
    page: int
    size: int


class AlertLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    site_id: int
    camera_id: int | None = None
    threshold_id: int | None = None
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    detected_at: datetime
    position_x: Decimal | None = None
    position_y: Decimal | None = None
    metadata_: dict[str, Any] | None = None
    is_acknowledged: bool
    acknowledged_by: int | None = None
    acknowledged_at: datetime | None = None
    created_at: datetime


class AlertLogListResponse(BaseModel):
    items: List[AlertLogResponse]
    total: int
    page: int
    size: int
