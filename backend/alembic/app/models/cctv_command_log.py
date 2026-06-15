from datetime import datetime
from typing import Any

from app.db.base import Base
from app.models.enums import CctvCommandStatus
from sqlalchemy import DateTime, Enum, ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CctvCommandLog(Base):
    __tablename__ = "cctv_command_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    camera_id: Mapped[int | None] = mapped_column(
        ForeignKey("cameras.id", ondelete="SET NULL"), nullable=True
    )
    nvr_id: Mapped[int | None] = mapped_column(
        ForeignKey("nvrs.id", ondelete="SET NULL"), nullable=True
    )

    command_type: Mapped[str] = mapped_column(String(50), nullable=False)
    request_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    response_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    status: Mapped[CctvCommandStatus] = mapped_column(
        Enum(CctvCommandStatus, name="cctv_command_status"),
        nullable=False,
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    requested_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    camera: Mapped["Camera | None"] = relationship("Camera")
    nvr: Mapped["NVR | None"] = relationship("NVR")
    requested_by_user: Mapped["User | None"] = relationship("User")

    __table_args__ = (
        Index("ix_cctv_command_logs_camera_id", "camera_id"),
        Index("ix_cctv_command_logs_nvr_id", "nvr_id"),
        Index("ix_cctv_command_logs_command_type", "command_type"),
        Index("ix_cctv_command_logs_status", "status"),
        Index("ix_cctv_command_logs_requested_at", "requested_at"),
    )


from app.models.camera import Camera  # noqa: E402
from app.models.nvr import NVR  # noqa: E402
from app.models.user import User  # noqa: E402
