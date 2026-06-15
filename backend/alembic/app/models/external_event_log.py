from datetime import datetime
from typing import Any

from app.db.base import Base
from app.models.enums import ExternalEventStatus
from sqlalchemy import DateTime, Enum, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class ExternalEventLog(Base):
    __tablename__ = "external_event_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    source_system: Mapped[str] = mapped_column(String(100), nullable=False)
    event_id: Mapped[str] = mapped_column(String(100), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")

    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    processed_status: Mapped[ExternalEventStatus] = mapped_column(
        Enum(ExternalEventStatus, name="external_event_status"),
        nullable=False,
        default=ExternalEventStatus.pending,
    )
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    related_entity_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    related_entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint("source_system", "event_id", name="uq_external_event_logs_source_event"),
        Index("ix_external_event_logs_event_type", "event_type"),
        Index("ix_external_event_logs_processed_status", "processed_status"),
        Index("ix_external_event_logs_received_at", "received_at"),
    )
