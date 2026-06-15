from datetime import datetime

from app.schemas.alert.base import AlertLogBase, AlertThresholdBase


class AlertThresholdCreate(AlertThresholdBase):
    created_by: int | None = None


class AlertLogCreate(AlertLogBase):
    detected_at: datetime
