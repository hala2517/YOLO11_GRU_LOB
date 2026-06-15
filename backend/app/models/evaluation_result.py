from datetime import datetime
from decimal import Decimal
from typing import Any

from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class EvaluationResult(TimestampMixin, Base):
    __tablename__ = "evaluation_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    model_id: Mapped[int] = mapped_column(
        ForeignKey("ai_models.id", ondelete="CASCADE"), nullable=False
    )
    dataset_id: Mapped[int | None] = mapped_column(
        ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True
    )
    training_job_id: Mapped[int | None] = mapped_column(
        ForeignKey("training_jobs.id", ondelete="SET NULL"), nullable=True
    )

    evaluation_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    # 주요 성능 지표
    mAP: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    precision: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    recall: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    f1_score: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    inference_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    accuracy: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)

    # 파일 스캔 자동 등록 필드
    source_file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    raw_metrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # 메타 정보
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_processed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationships
    model: Mapped["AIModel"] = relationship("AIModel", back_populates="evaluation_results")
    dataset: Mapped["Dataset | None"] = relationship("Dataset", back_populates="evaluation_results")
    training_job: Mapped["TrainingJob | None"] = relationship(
        "TrainingJob", back_populates="evaluation_results"
    )

    __table_args__ = (
        Index("ix_evaluation_results_model_id", "model_id"),
        Index("ix_evaluation_results_dataset_id", "dataset_id"),
        Index("ix_evaluation_results_training_job_id", "training_job_id"),
        Index("ix_evaluation_results_evaluation_date", "evaluation_date"),
        Index("ix_evaluation_results_file_hash", "file_hash"),
        Index("ix_evaluation_results_is_processed", "is_processed"),
    )


from app.models.ai_model import AIModel  # noqa: E402
from app.models.dataset import Dataset  # noqa: E402
from app.models.training_job import TrainingJob  # noqa: E402
