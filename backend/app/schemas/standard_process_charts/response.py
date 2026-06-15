from datetime import date, datetime
from decimal import Decimal
from typing import Any, List

from pydantic import BaseModel, ConfigDict


class StandardProcessChartStepResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chart_id: int
    step_no: int
    process_name: str
    worker_label: str | None = None
    standard_worker_count: int | None = None
    standard_time: Decimal | None = None
    route_description: str | None = None
    machine_name: str | None = None
    note: str | None = None
    created_at: datetime
    updated_at: datetime


class StandardProcessChartLayoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chart_id: int
    layout_type: str
    width: int
    height: int
    nodes: list[dict[str, Any]] | None = None
    edges: list[dict[str, Any]] | None = None
    created_at: datetime
    updated_at: datetime


class StandardProcessChartAttachmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chart_id: int
    file_url: str
    file_name: str | None = None
    file_type: str | None = None
    sort_order: int
    created_at: datetime
    updated_at: datetime


class StandardProcessChartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    line_code: str
    product_code: str
    product_name: str | None = None
    name: str
    version: str
    status: str
    owner_department: str | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    note: str | None = None
    created_by: int | None = None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    steps: list[StandardProcessChartStepResponse] = []
    layouts: list[StandardProcessChartLayoutResponse] = []
    attachments: list[StandardProcessChartAttachmentResponse] = []


class StandardProcessChartListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    line_code: str
    product_code: str
    product_name: str | None = None
    name: str
    version: str
    status: str
    owner_department: str | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    note: str | None = None
    created_by: int | None = None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    step_count: int = 0


class StandardProcessChartListResponse(BaseModel):
    items: List[StandardProcessChartListItem]
    total: int
    page: int
    size: int
