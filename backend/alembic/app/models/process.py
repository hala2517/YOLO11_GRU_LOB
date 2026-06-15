from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Process(TimestampMixin, Base):
    __tablename__ = "processes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id", ondelete="RESTRICT"), nullable=False
    )
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    line_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    site: Mapped["Site"] = relationship("Site", back_populates="processes")
    created_by_user: Mapped["User | None"] = relationship(
        "User", back_populates="processes", foreign_keys=[created_by]
    )
    process_flows: Mapped[list["ProcessFlow"]] = relationship(
        "ProcessFlow", back_populates="process", cascade="all, delete-orphan"
    )
    efficiency_metrics: Mapped[list["EfficiencyMetric"]] = relationship(
        "EfficiencyMetric", back_populates="process", cascade="all, delete-orphan"
    )
    worker_detections: Mapped[list["WorkerDetection"]] = relationship(
        "WorkerDetection", back_populates="process", cascade="save-update, merge"
    )

    __table_args__ = (
        UniqueConstraint("site_id", "code", name="uq_processes_site_code"),
        Index("ix_processes_site_id", "site_id"),
        Index("ix_processes_is_deleted", "is_deleted"),
        Index("ix_processes_is_active", "is_active"),
        Index("ix_processes_line_order", "line_order"),
    )


from app.models.efficiency_metric import EfficiencyMetric  # noqa: E402
from app.models.process_flow import ProcessFlow  # noqa: E402
from app.models.site import Site  # noqa: E402
from app.models.user import User  # noqa: E402
from app.models.worker_detection import WorkerDetection  # noqa: E402
