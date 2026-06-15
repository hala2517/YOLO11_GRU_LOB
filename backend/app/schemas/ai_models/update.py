from datetime import datetime
from decimal import Decimal

from app.models.enums import AIModelType
from pydantic import BaseModel


class AIModelUpdate(BaseModel):
    name: str | None = None
    version: str | None = None
    model_type: AIModelType | None = None
    description: str | None = None
    file_path: str | None = None
    file_size_bytes: int | None = None
    mAP: Decimal | None = None
    precision: Decimal | None = None
    recall: Decimal | None = None
    is_active: bool | None = None
    is_deployed: bool | None = None
    trained_at: datetime | None = None
