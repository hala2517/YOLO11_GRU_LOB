import datetime as dt
from decimal import Decimal

from app.models.enums import ShiftType
from pydantic import BaseModel, Field


class EfficiencyMetricCreate(BaseModel):
    process_id: int
    mes_sync_log_id: int | None = None
    date: dt.date
    shift: ShiftType = ShiftType.day
    daily_production: int | None = Field(default=None, ge=0)
    hourly_production: Decimal | None = Field(default=None, ge=0)
    worker_count: int | None = Field(default=None, ge=0)
    tact_time: Decimal | None = Field(default=None, ge=0)
    standard_time: Decimal | None = Field(default=None, ge=0)
    labor_productivity: Decimal | None = None
    lob: Decimal | None = Field(default=None, ge=0, le=1)
    eb: Decimal | None = Field(default=None, ge=0, le=1)
    capa_per_hr: Decimal | None = Field(default=None, ge=0)
    source: str | None = None
