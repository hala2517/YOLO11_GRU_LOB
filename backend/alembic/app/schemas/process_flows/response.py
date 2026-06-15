from datetime import datetime
from typing import Any, List

from pydantic import BaseModel, ConfigDict


class ProcessFlowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    process_id: int
    version: int
    floor_plan_image_path: str | None = None
    nodes: list[dict[str, Any]] | None = None
    edges: list[dict[str, Any]] | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    created_by: int | None = None
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class ProcessFlowListResponse(BaseModel):
    items: List[ProcessFlowResponse]
    total: int
    page: int
    size: int
