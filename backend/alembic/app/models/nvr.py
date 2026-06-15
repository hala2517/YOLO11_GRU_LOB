from datetime import datetime

from app.db.base import Base
from app.models.enums import DeviceStatus
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class NVR(TimestampMixin, Base):
    __tablename__ = "nvrs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="RESTRICT"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    port: Mapped[int | None] = mapped_column(Integer, nullable=True, default=554)

    username: Mapped[str | None] = mapped_column(String(50), nullable=True)
    encrypted_password: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[DeviceStatus] = mapped_column(
        Enum(DeviceStatus, name="device_status"),
        nullable=False,
        default=DeviceStatus.offline,
    )
    last_connected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    firmware_version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    storage_capacity_gb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    used_storage_gb: Mapped[int | None] = mapped_column(Integer, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    site: Mapped["Site"] = relationship("Site", back_populates="nvrs")
    cameras: Mapped[list["Camera"]] = relationship(
        "Camera", back_populates="nvr", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_nvrs_site_id", "site_id"),
        Index("ix_nvrs_status", "status"),
        Index("ix_nvrs_is_deleted", "is_deleted"),
    )


from app.models.camera import Camera  # noqa: E402
from app.models.site import Site  # noqa: E402
