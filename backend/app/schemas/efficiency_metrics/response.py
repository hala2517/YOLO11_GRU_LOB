import datetime as dt
from decimal import Decimal
from typing import List

from app.models.enums import ShiftType
from pydantic import BaseModel, ConfigDict


class EfficiencyMetricResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    process_id: int
    mes_sync_log_id: int | None = None
    date: dt.date
    shift: ShiftType
    daily_production: int | None = None
    hourly_production: Decimal | None = None
    worker_count: int | None = None
    tact_time: Decimal | None = None
    standard_time: Decimal | None = None
    labor_productivity: Decimal | None = None
    lob: Decimal | None = None
    eb: Decimal | None = None
    capa_per_hr: Decimal | None = None
    source: str | None = None
    created_at: dt.datetime
    updated_at: dt.datetime


class EfficiencyMetricListResponse(BaseModel):
    items: List[EfficiencyMetricResponse]
    total: int
    page: int
    size: int
