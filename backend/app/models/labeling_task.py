from datetime import datetime

from app.db.base import Base
from app.models.enums import LabelingTaskStatus
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LabelingTask(TimestampMixin, Base):
    __tablename__ = "labeling_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    dataset_id: Mapped[int] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[LabelingTaskStatus] = mapped_column(
        Enum(LabelingTaskStatus, name="labeling_task_status"),
        nullable=False,
        default=LabelingTaskStatus.pending,
    )

    assigned_to: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_images: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    labeled_images: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="labeling_tasks")
    assigned_to_user: Mapped["User | None"] = relationship(
        "User", back_populates="assigned_labeling_tasks", foreign_keys=[assigned_to]
    )
    created_by_user: Mapped["User | None"] = relationship(
        "User", back_populates="created_labeling_tasks", foreign_keys=[created_by]
    )
    annotations: Mapped[list["Annotation"]] = relationship(
        "Annotation", back_populates="labeling_task", cascade="all, delete-orphan"
    )
    recognition_logs: Mapped[list["RecognitionLog"]] = relationship(
        "RecognitionLog", back_populates="labeling_task", cascade="save-update, merge"
    )

    __table_args__ = (
        Index("ix_labeling_tasks_dataset_id", "dataset_id"),
        Index("ix_labeling_tasks_status", "status"),
        Index("ix_labeling_tasks_assigned_to", "assigned_to"),
        Index("ix_labeling_tasks_is_deleted", "is_deleted"),
    )


from app.models.annotation import Annotation  # noqa: E402
from app.models.dataset import Dataset  # noqa: E402
from app.models.recognition_log import RecognitionLog  # noqa: E402
from app.models.user import User  # noqa: E402
