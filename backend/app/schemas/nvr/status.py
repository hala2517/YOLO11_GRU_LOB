from app.models.enums import DeviceStatus
from pydantic import BaseModel


class NVRStatusUpdate(BaseModel):
    status: DeviceStatus
