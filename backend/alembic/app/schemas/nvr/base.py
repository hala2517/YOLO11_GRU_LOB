from pydantic import BaseModel, ConfigDict
from pydantic.networks import IPvAnyAddress


class NVRBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    site_id: int
    name: str
    description: str | None = None
    ip_address: IPvAnyAddress
    port: int | None = 554
    username: str | None = None
    model_name: str | None = None
    firmware_version: str | None = None
    storage_capacity_gb: int | None = None
    is_active: bool = True
