from datetime import date
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class StandardProcessChartUpdate(BaseModel):
    line_code: str | None = Field(default=None, max_length=50)
    product_code: str | None = Field(default=None, max_length=100)
    product_name: str | None = Field(default=None, max_length=255)
    name: str | None = Field(default=None, max_length=200)
    version: str | None = Field(default=None, max_length=50)
    status: str | None = Field(default=None, max_length=30)
    owner_department: str | None = Field(default=None, max_length=100)
    effective_from: date | None = None
    effective_to: date | None = None
    note: str | None = None


class StandardProcessChartStepUpdate(BaseModel):
    step_no: int | None = Field(default=None, ge=1)
    process_name: str | None = Field(default=None, max_length=200)
    worker_label: str | None = Field(default=None, max_length=100)
    standard_worker_count: int | None = Field(default=None, ge=0)
    standard_time: Decimal | None = Field(default=None, ge=0)
    route_description: str | None = None
    machine_name: str | None = Field(default=None, max_length=200)
    note: str | None = None


class StandardProcessChartLayoutUpsert(BaseModel):
    layout_type: str = Field(default="process_map", max_length=50)
    width: int = Field(default=560, ge=1)
    height: int = Field(default=328, ge=1)
    nodes: list[dict[str, Any]] | None = None
    edges: list[dict[str, Any]] | None = None
