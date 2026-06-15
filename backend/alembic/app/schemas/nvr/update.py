from app.models.enums import DeviceStatus
from pydantic import BaseModel, ConfigDict


class NVRUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: str | None = None
    ip_address: str | None = None
    port: int | None = None
    username: str | None = None
    password: str | None = None
    model_name: str | None = None
    firmware_version: str | None = None
    storage_capacity_gb: int | None = None
    used_storage_gb: int | None = None
    status: DeviceStatus | None = None
    is_active: bool | None = None
