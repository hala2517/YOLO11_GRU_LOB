import datetime as dt
from decimal import Decimal

from app.db.base import Base
from app.models.enums import ShiftType
from app.models.timestamp import TimestampMixin
from sqlalchemy import Date, Enum, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class EfficiencyMetric(TimestampMixin, Base):
    __tablename__ = "efficiency_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    process_id: Mapped[int] = mapped_column(
        ForeignKey("processes.id", ondelete="RESTRICT"), nullable=False
    )
    mes_sync_log_id: Mapped[int | None] = mapped_column(
        ForeignKey("mes_sync_logs.id", ondelete="SET NULL"), nullable=True
    )

    date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    shift: Mapped[ShiftType] = mapped_column(
        Enum(ShiftType, name="shift_type"),
        nullable=False,
        default=ShiftType.day,
    )

    daily_production: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hourly_production: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    worker_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    tact_time: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    standard_time: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)

    labor_productivity: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    lob: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    eb: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    capa_per_hr: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    source: Mapped[str | None] = mapped_column(String(50), nullable=True)

    process: Mapped["Process"] = relationship("Process", back_populates="efficiency_metrics")
    mes_sync_log: Mapped["MesSyncLog | None"] = relationship(
        "MesSyncLog", back_populates="efficiency_metrics"
    )

    __table_args__ = (
        Index("ix_efficiency_metrics_process_id", "process_id"),
        Index("ix_efficiency_metrics_mes_sync_log_id", "mes_sync_log_id"),
        Index("ix_efficiency_metrics_date", "date"),
        Index("ix_efficiency_metrics_shift", "shift"),
        Index("ix_efficiency_metrics_date_process", "date", "process_id"),
    )


from app.models.mes_sync_log import MesSyncLog  # noqa: E402
from app.models.process import Process  # noqa: E402
