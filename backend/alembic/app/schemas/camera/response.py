from datetime import datetime
from decimal import Decimal
from typing import List

from app.models.enums import DeviceStatus
from pydantic import BaseModel, ConfigDict


class CameraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nvr_id: int
    site_id: int
    name: str
    camera_code: str | None = None
    channel: int | None = None
    rtsp_url: str | None = None
    location: str | None = None
    position_x: Decimal | None = None
    position_y: Decimal | None = None
    resolution: str | None = None
    fps: int | None = None
    model_name: str | None = None
    status: DeviceStatus
    last_connected_at: datetime | None = None
    is_active: bool
    created_at: datetime


class CameraListResponse(BaseModel):
    items: List[CameraResponse]
    total: int
    page: int
    size: int
