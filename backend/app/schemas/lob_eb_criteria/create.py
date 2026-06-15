from decimal import Decimal

from pydantic import BaseModel, Field


class LobEbCriteriaCreate(BaseModel):
    site_id: int | None = None
    line_code: str | None = Field(default=None, max_length=50)
    product_code: str | None = Field(default=None, max_length=100)
    lob_target: Decimal = Field(ge=0, le=100)
    lob_warning: Decimal = Field(ge=0, le=100)
    eb_target: Decimal = Field(ge=0, le=100)
    eb_warning: Decimal = Field(ge=0, le=100)
    takt_time_limit: Decimal | None = Field(default=None, ge=0)
    description: str | None = None
    is_active: bool = True
