from datetime import datetime
from typing import Any

from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProcessFlow(TimestampMixin, Base):
    __tablename__ = "process_flows"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    process_id: Mapped[int] = mapped_column(
        ForeignKey("processes.id", ondelete="CASCADE"), nullable=False
    )
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    floor_plan_image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    nodes: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)
    edges: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)

    effective_from: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    process: Mapped["Process"] = relationship("Process", back_populates="process_flows")
    created_by_user: Mapped["User | None"] = relationship(
        "User", back_populates="process_flows", foreign_keys=[created_by]
    )

    __table_args__ = (
        UniqueConstraint("process_id", "version", name="uq_process_flows_process_version"),
        Index("ix_process_flows_process_id", "process_id"),
        Index("ix_process_flows_is_active", "is_active"),
        Index("ix_process_flows_is_deleted", "is_deleted"),
        Index("ix_process_flows_effective_from", "effective_from"),
    )


from app.models.process import Process  # noqa: E402
from app.models.user import User  # noqa: E402
