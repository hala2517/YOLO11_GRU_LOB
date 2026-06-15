from datetime import datetime
from typing import Any

from app.db.base import Base
from app.models.enums import MesSyncStatus
from sqlalchemy import DateTime, Enum, ForeignKey, Index, JSON, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MesSyncLog(Base):
    __tablename__ = "mes_sync_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="RESTRICT"), nullable=False
    )

    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    processed_status: Mapped[MesSyncStatus] = mapped_column(
        Enum(MesSyncStatus, name="mes_sync_status"),
        nullable=False,
        default=MesSyncStatus.pending,
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    site: Mapped["Site"] = relationship("Site", back_populates="mes_sync_logs")
    efficiency_metrics: Mapped[list["EfficiencyMetric"]] = relationship(
        "EfficiencyMetric", back_populates="mes_sync_log", cascade="save-update, merge"
    )

    __table_args__ = (
        Index("ix_mes_sync_logs_site_id", "site_id"),
        Index("ix_mes_sync_logs_processed_status", "processed_status"),
        Index("ix_mes_sync_logs_created_at", "created_at"),
    )


from app.models.efficiency_metric import EfficiencyMetric  # noqa: E402
from app.models.site import Site  # noqa: E402
