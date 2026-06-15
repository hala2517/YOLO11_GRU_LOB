from datetime import date
from decimal import Decimal
from typing import Any

from app.db.base import Base
from app.models.timestamp import TimestampMixin
from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class StandardProcessChart(TimestampMixin, Base):
    __tablename__ = "standard_process_charts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    line_code: Mapped[str] = mapped_column(String(50), nullable=False)
    product_code: Mapped[str] = mapped_column(String(100), nullable=False)
    product_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft")
    owner_department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    effective_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_by_user: Mapped["User | None"] = relationship("User")
    steps: Mapped[list["StandardProcessChartStep"]] = relationship(
        "StandardProcessChartStep",
        back_populates="chart",
        cascade="all, delete-orphan",
        order_by="StandardProcessChartStep.step_no",
    )
    layouts: Mapped[list["StandardProcessChartLayout"]] = relationship(
        "StandardProcessChartLayout",
        back_populates="chart",
        cascade="all, delete-orphan",
    )
    attachments: Mapped[list["StandardProcessChartAttachment"]] = relationship(
        "StandardProcessChartAttachment",
        back_populates="chart",
        cascade="all, delete-orphan",
        order_by="StandardProcessChartAttachment.sort_order",
    )

    __table_args__ = (
        UniqueConstraint(
            "line_code",
            "product_code",
            "version",
            name="uq_standard_process_charts_line_product_version",
        ),
        Index("ix_standard_process_charts_line_code", "line_code"),
        Index("ix_standard_process_charts_product_code", "product_code"),
        Index("ix_standard_process_charts_status", "status"),
        Index("ix_standard_process_charts_is_deleted", "is_deleted"),
    )


class StandardProcessChartStep(TimestampMixin, Base):
    __tablename__ = "standard_process_chart_steps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chart_id: Mapped[int] = mapped_column(
        ForeignKey("standard_process_charts.id", ondelete="CASCADE"), nullable=False
    )

    step_no: Mapped[int] = mapped_column(Integer, nullable=False)
    process_name: Mapped[str] = mapped_column(String(200), nullable=False)
    worker_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    standard_worker_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    standard_time: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    route_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    machine_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    chart: Mapped["StandardProcessChart"] = relationship(
        "StandardProcessChart", back_populates="steps"
    )

    __table_args__ = (
        UniqueConstraint("chart_id", "step_no", name="uq_standard_process_chart_steps_chart_step"),
        Index("ix_standard_process_chart_steps_chart_id", "chart_id"),
    )


class StandardProcessChartLayout(TimestampMixin, Base):
    __tablename__ = "standard_process_chart_layouts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chart_id: Mapped[int] = mapped_column(
        ForeignKey("standard_process_charts.id", ondelete="CASCADE"), nullable=False
    )

    layout_type: Mapped[str] = mapped_column(String(50), nullable=False, default="process_map")
    width: Mapped[int] = mapped_column(Integer, nullable=False, default=560)
    height: Mapped[int] = mapped_column(Integer, nullable=False, default=328)
    nodes: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)
    edges: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)

    chart: Mapped["StandardProcessChart"] = relationship(
        "StandardProcessChart", back_populates="layouts"
    )

    __table_args__ = (
        UniqueConstraint("chart_id", "layout_type", name="uq_standard_process_chart_layouts_chart_type"),
        Index("ix_standard_process_chart_layouts_chart_id", "chart_id"),
    )


class StandardProcessChartAttachment(TimestampMixin, Base):
    __tablename__ = "standard_process_chart_attachments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chart_id: Mapped[int] = mapped_column(
        ForeignKey("standard_process_charts.id", ondelete="CASCADE"), nullable=False
    )

    file_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    chart: Mapped["StandardProcessChart"] = relationship(
        "StandardProcessChart", back_populates="attachments"
    )

    __table_args__ = (
        Index("ix_standard_process_chart_attachments_chart_id", "chart_id"),
        Index("ix_standard_process_chart_attachments_sort_order", "sort_order"),
    )


from app.models.user import User  # noqa: E402
