from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class RoleListResponse(BaseModel):
    items: List[RoleResponse]
    total: int
    page: int
    size: int
