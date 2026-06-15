from datetime import datetime
from decimal import Decimal

from app.db.base import Base
from app.models.enums import DeviceStatus
from app.models.timestamp import TimestampMixin
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Camera(TimestampMixin, Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nvr_id: Mapped[int] = mapped_column(
        ForeignKey("nvrs.id", ondelete="CASCADE"), nullable=False
    )
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="RESTRICT"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    camera_code: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    channel: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rtsp_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    position_x: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    position_y: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    resolution: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fps: Mapped[int | None] = mapped_column(Integer, nullable=True, default=30)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    status: Mapped[DeviceStatus] = mapped_column(
        Enum(DeviceStatus, name="device_status"),
        nullable=False,
        default=DeviceStatus.offline,
    )
    last_connected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    nvr: Mapped["NVR"] = relationship("NVR", back_populates="cameras")
    site: Mapped["Site"] = relationship("Site", back_populates="cameras")
    alert_logs: Mapped[list["AlertLog"]] = relationship(
        "AlertLog", back_populates="camera", cascade="save-update, merge"
    )
    data_collection_jobs: Mapped[list["DataCollectionJob"]] = relationship(
        "DataCollectionJob", back_populates="camera", cascade="all, delete-orphan"
    )
    recognition_logs: Mapped[list["RecognitionLog"]] = relationship(
        "RecognitionLog", back_populates="camera", cascade="save-update, merge"
    )
    worker_detections: Mapped[list["WorkerDetection"]] = relationship(
        "WorkerDetection", back_populates="camera", cascade="save-update, merge"
    )
    collected_videos: Mapped[list["CollectedVideo"]] = relationship(
        "CollectedVideo", back_populates="camera", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_cameras_nvr_id", "nvr_id"),
        Index("ix_cameras_site_id", "site_id"),
        Index("ix_cameras_camera_code", "camera_code"),
        Index("ix_cameras_status", "status"),
        Index("ix_cameras_is_deleted", "is_deleted"),
    )


from app.models.alert import AlertLog  # noqa: E402
from app.models.data_collection_job import DataCollectionJob  # noqa: E402
from app.models.nvr import NVR  # noqa: E402
from app.models.recognition_log import RecognitionLog  # noqa: E402
from app.models.site import Site  # noqa: E402
from app.models.collected_video import CollectedVideo  # noqa: E402
from app.models.worker_detection import WorkerDetection  # noqa: E402
