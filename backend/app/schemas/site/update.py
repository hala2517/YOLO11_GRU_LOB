from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SiteUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    code: str | None = None
    description: str | None = None
    address: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    floor_plan_image_path: str | None = None
    is_active: bool | None = None
