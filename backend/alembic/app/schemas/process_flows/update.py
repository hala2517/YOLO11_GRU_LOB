from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ProcessFlowUpdate(BaseModel):
    floor_plan_image_path: str | None = None
    nodes: list[dict[str, Any]] | None = None
    edges: list[dict[str, Any]] | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    is_active: bool | None = None
