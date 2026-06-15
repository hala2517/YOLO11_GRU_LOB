from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict


class LobEbCriteriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    site_id: int | None = None
    line_code: str | None = None
    product_code: str | None = None
    lob_target: Decimal
    lob_warning: Decimal
    eb_target: Decimal
    eb_warning: Decimal
    takt_time_limit: Decimal | None = None
    description: str | None = None
    is_active: bool
    created_by: int | None = None
    created_at: datetime
    updated_at: datetime


class LobEbCriteriaListResponse(BaseModel):
    items: List[LobEbCriteriaResponse]
    total: int
    page: int
    size: int
