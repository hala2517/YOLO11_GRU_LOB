from decimal import Decimal
from typing import Any

from app.models.enums import AlertSeverity, AlertType
from pydantic import BaseModel, ConfigDict


class AlertThresholdBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    site_id: int
    alert_type: AlertType
    name: str
    description: str | None = None
    threshold_value: Decimal | None = None
    threshold_unit: str | None = None
    color_value: str | None = None
    conditions: dict[str, Any] | None = None
    is_active: bool = True


class AlertLogBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    site_id: int
    camera_id: int | None = None
    threshold_id: int | None = None
    alert_type: AlertType
    severity: AlertSeverity = AlertSeverity.medium
    title: str
    message: str
    position_x: Decimal | None = None
    position_y: Decimal | None = None
    metadata_: dict[str, Any] | None = None
