from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CameraBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nvr_id: int
    name: str
    camera_code: str | None = None
    channel: int | None = None
    rtsp_url: str | None = None
    location: str | None = None
    position_x: Decimal | None = None
    position_y: Decimal | None = None
    resolution: str | None = None
    fps: int | None = 30
    model_name: str | None = None
    is_active: bool = True
