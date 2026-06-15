from datetime import datetime
from decimal import Decimal
from typing import Any, List

from pydantic import BaseModel, ConfigDict


class EvaluationResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model_id: int
    dataset_id: int | None = None
    training_job_id: int | None = None

    evaluation_date: datetime

    mAP: Decimal | None = None
    precision: Decimal | None = None
    recall: Decimal | None = None
    f1_score: Decimal | None = None
    inference_time_ms: int | None = None
    accuracy: Decimal | None = None

    # 파일 스캔 자동 등록 필드
    source_file_path: str
    file_hash: str | None = None
    raw_metrics: dict[str, Any]

    # 메타 정보
    notes: str | None = None
    is_processed: bool

    created_at: datetime
    updated_at: datetime


class EvaluationResultListResponse(BaseModel):
    items: List[EvaluationResultResponse]
    total: int
    page: int
    size: int
