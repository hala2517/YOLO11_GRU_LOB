from datetime import datetime
from typing import Any

from app.db.base import Base
from app.models.enums import TrainingJobStatus
from app.models.timestamp import TimestampMixin
from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TrainingJob(TimestampMixin, Base):
    __tablename__ = "training_jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_name: Mapped[str] = mapped_column(String(100), nullable=False)

    model_id: Mapped[int | None] = mapped_column(
        ForeignKey("ai_models.id", ondelete="SET NULL"), nullable=True
    )
    dataset_id: Mapped[int] = mapped_column(
        ForeignKey("datasets.id"), nullable=False
    )

    status: Mapped[TrainingJobStatus] = mapped_column(
        Enum(TrainingJobStatus, name="training_job_status"),
        nullable=False,
        default=TrainingJobStatus.pending,
    )

    parameters: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    metrics: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    external_job_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_system: Mapped[str | None] = mapped_column(String(100), nullable=True)
    raw_events: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    model: Mapped["AIModel | None"] = relationship("AIModel", back_populates="training_jobs")
    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="training_jobs")
    created_by_user: Mapped["User | None"] = relationship(
        "User", back_populates="training_jobs", foreign_keys=[created_by]
    )
    evaluation_results: Mapped[list["EvaluationResult"]] = relationship(
        "EvaluationResult", back_populates="training_job", cascade="save-update, merge"
    )

    __table_args__ = (
        Index("ix_training_jobs_status", "status"),
        Index("ix_training_jobs_dataset_id", "dataset_id"),
        Index("ix_training_jobs_model_id", "model_id"),
        Index("ix_training_jobs_external_job_id", "external_job_id"),
    )


from app.models.ai_model import AIModel  # noqa: E402
from app.models.dataset import Dataset  # noqa: E402
from app.models.evaluation_result import EvaluationResult  # noqa: E402
from app.models.user import User  # noqa: E402
