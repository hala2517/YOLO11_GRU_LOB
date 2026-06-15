from decimal import Decimal

from app.models.enums import DeviceStatus
from pydantic import BaseModel, ConfigDict


class CameraUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    camera_code: str | None = None
    channel: int | None = None
    rtsp_url: str | None = None
    location: str | None = None
    position_x: Decimal | None = None
    position_y: Decimal | None = None
    resolution: str | None = None
    fps: int | None = None
    model_name: str | None = None
    status: DeviceStatus | None = None
    is_active: bool | None = None
