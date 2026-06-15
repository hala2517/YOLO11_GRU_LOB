from decimal import Decimal

from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Site(TimestampMixin, Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    code: Mapped[str | None] = mapped_column(String(20), nullable=True, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 8), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(11, 8), nullable=True)
    floor_plan_image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    nvrs: Mapped[list["NVR"]] = relationship(
        "NVR", back_populates="site", cascade="save-update, merge"
    )
    cameras: Mapped[list["Camera"]] = relationship(
        "Camera", back_populates="site", cascade="save-update, merge"
    )
    alert_thresholds: Mapped[list["AlertThreshold"]] = relationship(
        "AlertThreshold", back_populates="site", cascade="all, delete-orphan"
    )
    alert_logs: Mapped[list["AlertLog"]] = relationship(
        "AlertLog", back_populates="site", cascade="save-update, merge"
    )
    recognition_logs: Mapped[list["RecognitionLog"]] = relationship(
        "RecognitionLog", back_populates="site", cascade="save-update, merge"
    )
    processes: Mapped[list["Process"]] = relationship(
        "Process", back_populates="site", cascade="all, delete-orphan"
    )
    mes_sync_logs: Mapped[list["MesSyncLog"]] = relationship(
        "MesSyncLog", back_populates="site", cascade="save-update, merge"
    )
    worker_detections: Mapped[list["WorkerDetection"]] = relationship(
        "WorkerDetection", back_populates="site", cascade="save-update, merge"
    )
    collected_videos: Mapped[list["CollectedVideo"]] = relationship(
        "CollectedVideo", back_populates="site", cascade="save-update, merge"
    )

    __table_args__ = (
        Index("ix_sites_name", "name"),
        Index("ix_sites_code", "code"),
        Index("ix_sites_is_deleted", "is_deleted"),
    )


from app.models.alert import AlertLog, AlertThreshold  # noqa: E402
from app.models.camera import Camera  # noqa: E402
from app.models.nvr import NVR  # noqa: E402
from app.models.collected_video import CollectedVideo  # noqa: E402
from app.models.mes_sync_log import MesSyncLog  # noqa: E402
from app.models.process import Process  # noqa: E402
from app.models.recognition_log import RecognitionLog  # noqa: E402
from app.models.worker_detection import WorkerDetection  # noqa: E402
