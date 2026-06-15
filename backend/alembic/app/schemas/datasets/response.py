from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class DatasetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    total_images: int
    labeled_images: int
    storage_path: str | None = None
    version: str | None = None
    is_active: bool
    created_by: int | None = None
    created_at: datetime
    updated_at: datetime


class DatasetListResponse(BaseModel):
    items: List[DatasetResponse]
    total: int
    page: int
    size: int
