from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SiteBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    code: str | None = None
    description: str | None = None
    address: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    floor_plan_image_path: str | None = None
    is_active: bool = True
