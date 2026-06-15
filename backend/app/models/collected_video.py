from datetime import datetime

from app.db.base import Base
from app.models.enums import CollectedVideoStatus
from app.models.timestamp import TimestampMixin
from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CollectedVideo(TimestampMixin, Base):
    __tablename__ = "collected_videos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    camera_id: Mapped[int] = mapped_column(
        ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False
    )
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="RESTRICT"), nullable=False
    )
    data_collection_job_id: Mapped[int | None] = mapped_column(
        ForeignKey("data_collection_jobs.id", ondelete="SET NULL"), nullable=True
    )
    recognition_log_id: Mapped[int | None] = mapped_column(
        ForeignKey("recognition_logs.id", ondelete="SET NULL"), nullable=True
    )

    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    resolution: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fps: Mapped[int | None] = mapped_column(Integer, nullable=True)
    storage_type: Mapped[str] = mapped_column(String(20), nullable=False, default="local")

    status: Mapped[CollectedVideoStatus] = mapped_column(
        Enum(CollectedVideoStatus, name="collected_video_status"),
        nullable=False,
        default=CollectedVideoStatus.pending,
    )

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    camera: Mapped["Camera"] = relationship("Camera", back_populates="collected_videos")
    site: Mapped["Site"] = relationship("Site", back_populates="collected_videos")
    data_collection_job: Mapped["DataCollectionJob | None"] = relationship(
        "DataCollectionJob", back_populates="collected_videos"
    )
    recognition_log: Mapped["RecognitionLog | None"] = relationship(
        "RecognitionLog", back_populates="collected_videos"
    )

    __table_args__ = (
        Index("ix_collected_videos_camera_id", "camera_id"),
        Index("ix_collected_videos_site_id", "site_id"),
        Index("ix_collected_videos_data_collection_job_id", "data_collection_job_id"),
        Index("ix_collected_videos_recorded_at", "recorded_at"),
        Index("ix_collected_videos_status", "status"),
        Index("ix_collected_videos_is_deleted", "is_deleted"),
        Index("ix_collected_videos_camera_recorded", "camera_id", "recorded_at"),
    )


from app.models.camera import Camera  # noqa: E402
from app.models.data_collection_job import DataCollectionJob  # noqa: E402
from app.models.recognition_log import RecognitionLog  # noqa: E402
from app.models.site import Site  # noqa: E402
