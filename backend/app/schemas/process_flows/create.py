from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ProcessFlowCreate(BaseModel):
    process_id: int
    version: int = Field(default=1, ge=1)
    floor_plan_image_path: str | None = None
    nodes: list[dict[str, Any]] | None = None
    edges: list[dict[str, Any]] | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    created_by: int | None = None
    is_active: bool = True
