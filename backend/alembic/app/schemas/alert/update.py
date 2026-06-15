from decimal import Decimal
from typing import Any

from app.models.enums import AlertType
from pydantic import BaseModel, ConfigDict


class AlertThresholdUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    alert_type: AlertType | None = None
    name: str | None = None
    description: str | None = None
    threshold_value: Decimal | None = None
    threshold_unit: str | None = None
    color_value: str | None = None
    conditions: dict[str, Any] | None = None
    is_active: bool | None = None


class AlertLogUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    is_acknowledged: bool | None = None
    acknowledged_by: int | None = None
