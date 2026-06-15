from datetime import datetime
from typing import List

from app.models.enums import DeviceStatus
from pydantic import BaseModel, ConfigDict
from pydantic.networks import IPvAnyAddress


class NVRResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    site_id: int
    name: str
    description: str | None = None
    ip_address: IPvAnyAddress
    port: int | None = None
    username: str | None = None
    status: DeviceStatus
    last_connected_at: datetime | None = None
    model_name: str | None = None
    storage_capacity_gb: int | None = None
    used_storage_gb: int | None = None
    is_active: bool
    created_at: datetime


class NVRListResponse(BaseModel):
    items: List[NVRResponse]
    total: int
    page: int
    size: int
