from datetime import datetime

from app.db.base import Base
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class WorkerDetection(Base):
    __tablename__ = "worker_detections"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    recognition_log_id: Mapped[int | None] = mapped_column(
        ForeignKey("recognition_logs.id", ondelete="SET NULL"), nullable=True
    )
    process_id: Mapped[int | None] = mapped_column(
        ForeignKey("processes.id", ondelete="SET NULL"), nullable=True
    )
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="RESTRICT"), nullable=False
    )
    camera_id: Mapped[int] = mapped_column(
        ForeignKey("cameras.id", ondelete="RESTRICT"), nullable=False
    )

    worker_label: Mapped[str | None] = mapped_column(String(100), nullable=True)

    entry_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    exit_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    recognition_log: Mapped["RecognitionLog | None"] = relationship(
        "RecognitionLog", back_populates="worker_detections"
    )
    process: Mapped["Process | None"] = relationship(
        "Process", back_populates="worker_detections"
    )
    site: Mapped["Site"] = relationship("Site", back_populates="worker_detections")
    camera: Mapped["Camera"] = relationship("Camera", back_populates="worker_detections")

    __table_args__ = (
        Index("ix_worker_detections_process_id", "process_id"),
        Index("ix_worker_detections_site_id", "site_id"),
        Index("ix_worker_detections_camera_id", "camera_id"),
        Index("ix_worker_detections_entry_time", "entry_time"),
        Index("ix_worker_detections_recognition_log_id", "recognition_log_id"),
    )


from app.models.camera import Camera  # noqa: E402
from app.models.process import Process  # noqa: E402
from app.models.recognition_log import RecognitionLog  # noqa: E402
from app.models.site import Site  # noqa: E402
