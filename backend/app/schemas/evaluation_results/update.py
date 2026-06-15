from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel


class EvaluationResultUpdate(BaseModel):
    dataset_id: int | None = None
    training_job_id: int | None = None

    evaluation_date: datetime | None = None

    mAP: Decimal | None = None
    precision: Decimal | None = None
    recall: Decimal | None = None
    f1_score: Decimal | None = None
    inference_time_ms: int | None = None
    accuracy: Decimal | None = None

    # 파일 스캔 자동 등록 필드
    source_file_path: str | None = None
    file_hash: str | None = None
    raw_metrics: dict[str, Any] | None = None

    # 메타 정보
    notes: str | None = None
    is_processed: bool | None = None
