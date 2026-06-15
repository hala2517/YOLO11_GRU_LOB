from datetime import datetime
from decimal import Decimal
from typing import Any

from app.db.base import Base
from app.models.enums import RecognitionType
from sqlalchemy import DateTime, Enum, ForeignKey, Index, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RecognitionLog(Base):
    __tablename__ = "recognition_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="RESTRICT"), nullable=False
    )
    camera_id: Mapped[int] = mapped_column(
        ForeignKey("cameras.id", ondelete="RESTRICT"), nullable=False
    )
    labeling_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("labeling_tasks.id", ondelete="SET NULL"), nullable=True
    )

    recognition_type: Mapped[RecognitionType] = mapped_column(
        Enum(RecognitionType, name="recognition_type"),
        nullable=False,
    )

    class_name: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)

    bbox: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    position_x: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    position_y: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    metadata_: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata", JSON, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    site: Mapped["Site"] = relationship("Site", back_populates="recognition_logs")
    camera: Mapped["Camera"] = relationship("Camera", back_populates="recognition_logs")
    labeling_task: Mapped["LabelingTask | None"] = relationship(
        "LabelingTask", back_populates="recognition_logs"
    )
    worker_detections: Mapped[list["WorkerDetection"]] = relationship(
        "WorkerDetection", back_populates="recognition_log", cascade="save-update, merge"
    )
    collected_videos: Mapped[list["CollectedVideo"]] = relationship(
        "CollectedVideo", back_populates="recognition_log", cascade="save-update, merge"
    )

    __table_args__ = (
        Index("ix_recognition_logs_site_id", "site_id"),
        Index("ix_recognition_logs_camera_id", "camera_id"),
        Index("ix_recognition_logs_recognition_type", "recognition_type"),
        Index("ix_recognition_logs_detected_at", "detected_at"),
        Index("ix_recognition_logs_labeling_task_id", "labeling_task_id"),
    )


from app.models.camera import Camera  # noqa: E402
from app.models.collected_video import CollectedVideo  # noqa: E402
from app.models.labeling_task import LabelingTask  # noqa: E402
from app.models.site import Site  # noqa: E402
from app.models.worker_detection import WorkerDetection  # noqa: E402
