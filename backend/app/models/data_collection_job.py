from datetime import datetime

from app.db.base import Base
from app.models.enums import DataCollectionJobStatus
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DataCollectionJob(TimestampMixin, Base):
    __tablename__ = "data_collection_jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    camera_id: Mapped[int] = mapped_column(
        ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False
    )
    dataset_id: Mapped[int | None] = mapped_column(
        ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True
    )

    job_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[DataCollectionJobStatus] = mapped_column(
        Enum(DataCollectionJobStatus, name="data_collection_job_status"),
        nullable=False,
        default=DataCollectionJobStatus.pending,
    )

    schedule_cron: Mapped[str | None] = mapped_column(String(100), nullable=True)
    interval_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    total_captured: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    camera: Mapped["Camera"] = relationship("Camera", back_populates="data_collection_jobs")
    dataset: Mapped["Dataset | None"] = relationship("Dataset", back_populates="data_collection_jobs")
    created_by_user: Mapped["User | None"] = relationship(
        "User", back_populates="data_collection_jobs", foreign_keys=[created_by]
    )
    collected_videos: Mapped[list["CollectedVideo"]] = relationship(
        "CollectedVideo", back_populates="data_collection_job", cascade="save-update, merge"
    )

    __table_args__ = (
        Index("ix_data_collection_jobs_camera_id", "camera_id"),
        Index("ix_data_collection_jobs_dataset_id", "dataset_id"),
        Index("ix_data_collection_jobs_status", "status"),
        Index("ix_data_collection_jobs_is_deleted", "is_deleted"),
    )


from app.models.camera import Camera  # noqa: E402
from app.models.collected_video import CollectedVideo  # noqa: E402
from app.models.dataset import Dataset  # noqa: E402
from app.models.user import User  # noqa: E402
