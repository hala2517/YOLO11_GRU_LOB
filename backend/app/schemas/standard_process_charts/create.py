from datetime import date
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class StandardProcessChartStepCreate(BaseModel):
    step_no: int = Field(ge=1)
    process_name: str = Field(max_length=200)
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


class StandardProcessChartAttachmentCreate(BaseModel):
    file_url: str = Field(max_length=1000)
    file_name: str | None = Field(default=None, max_length=255)
    file_type: str | None = Field(default=None, max_length=50)
    sort_order: int = Field(default=0, ge=0)


class StandardProcessChartCreate(BaseModel):
    line_code: str = Field(max_length=50)
    product_code: str = Field(max_length=100)
    product_name: str | None = Field(default=None, max_length=255)
    name: str = Field(max_length=200)
    version: str = Field(max_length=50)
    status: str = Field(default="draft", max_length=30)
    owner_department: str | None = Field(default=None, max_length=100)
    effective_from: date | None = None
    effective_to: date | None = None
    note: str | None = None
    steps: list[StandardProcessChartStepCreate] = Field(default_factory=list)
    layout: StandardProcessChartLayoutUpsert | None = None
    attachments: list[StandardProcessChartAttachmentCreate] = Field(default_factory=list)
