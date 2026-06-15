from datetime import datetime

from app.db.base import Base
from app.models.enums import StreamSessionStatus
from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class StreamSession(Base):
    __tablename__ = "stream_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    camera_id: Mapped[int] = mapped_column(
        ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False
    )

    stream_type: Mapped[str] = mapped_column(String(20), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    playback_url: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[StreamSessionStatus] = mapped_column(
        Enum(StreamSessionStatus, name="stream_session_status"),
        nullable=False,
        default=StreamSessionStatus.running,
    )

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    stopped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    camera: Mapped["Camera"] = relationship("Camera")

    __table_args__ = (
        Index("ix_stream_sessions_camera_id", "camera_id"),
        Index("ix_stream_sessions_status", "status"),
        Index("ix_stream_sessions_last_accessed_at", "last_accessed_at"),
    )


from app.models.camera import Camera  # noqa: E402
