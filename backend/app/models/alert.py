from datetime import datetime
from decimal import Decimal
from typing import Any

from app.db.base import Base
from app.models.enums import AlertSeverity, AlertType
from app.models.timestamp import TimestampMixin
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AlertThreshold(TimestampMixin, Base):
    __tablename__ = "alert_thresholds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"), nullable=False
    )

    alert_type: Mapped[AlertType] = mapped_column(
        Enum(AlertType, name="alert_type"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    threshold_value: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    threshold_unit: Mapped[str | None] = mapped_column(String(20), nullable=True)
    color_value: Mapped[str | None] = mapped_column(String(20), nullable=True)
    conditions: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    site: Mapped["Site"] = relationship("Site", back_populates="alert_thresholds")
    created_by_user: Mapped["User | None"] = relationship(
        "User",
        back_populates="created_alert_thresholds",
        foreign_keys=[created_by],
    )
    alert_logs: Mapped[list["AlertLog"]] = relationship(
        "AlertLog", back_populates="threshold", cascade="save-update, merge"
    )

    __table_args__ = (
        Index("ix_alert_thresholds_site_id", "site_id"),
        Index("ix_alert_thresholds_alert_type", "alert_type"),
        Index("ix_alert_thresholds_is_active", "is_active"),
    )


class AlertLog(Base):
    __tablename__ = "alert_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="RESTRICT"), nullable=False
    )
    camera_id: Mapped[int | None] = mapped_column(
        ForeignKey("cameras.id", ondelete="SET NULL"), nullable=True
    )
    threshold_id: Mapped[int | None] = mapped_column(
        ForeignKey("alert_thresholds.id", ondelete="SET NULL"), nullable=True
    )

    alert_type: Mapped[AlertType] = mapped_column(
        Enum(AlertType, name="alert_type"), nullable=False
    )
    severity: Mapped[AlertSeverity] = mapped_column(
        Enum(AlertSeverity, name="alert_severity"),
        nullable=False,
        default=AlertSeverity.medium,
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    position_x: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    position_y: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    metadata_: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata", JSON, nullable=True
    )

    is_acknowledged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    acknowledged_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    site: Mapped["Site"] = relationship("Site", back_populates="alert_logs")
    camera: Mapped["Camera | None"] = relationship("Camera", back_populates="alert_logs")
    threshold: Mapped["AlertThreshold | None"] = relationship(
        "AlertThreshold", back_populates="alert_logs"
    )
    acknowledged_by_user: Mapped["User | None"] = relationship(
        "User",
        back_populates="acknowledged_alert_logs",
        foreign_keys=[acknowledged_by],
    )

    __table_args__ = (
        Index("ix_alert_logs_site_id", "site_id"),
        Index("ix_alert_logs_camera_id", "camera_id"),
        Index("ix_alert_logs_alert_type", "alert_type"),
        Index("ix_alert_logs_severity", "severity"),
        Index("ix_alert_logs_detected_at", "detected_at"),
        Index("ix_alert_logs_is_acknowledged", "is_acknowledged"),
    )


from app.models.camera import Camera  # noqa: E402
from app.models.site import Site  # noqa: E402
from app.models.user import User  # noqa: E402
