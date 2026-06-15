from datetime import datetime
from decimal import Decimal

from app.models.enums import AIModelType
from pydantic import BaseModel


class AIModelCreate(BaseModel):
    name: str
    version: str
    model_type: AIModelType
    description: str | None = None
    file_path: str
    file_size_bytes: int | None = None
    mAP: Decimal | None = None
    precision: Decimal | None = None
    recall: Decimal | None = None
    is_active: bool = True
    is_deployed: bool = False
    trained_at: datetime | None = None
