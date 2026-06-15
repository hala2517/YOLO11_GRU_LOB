from datetime import datetime, timezone

from app.models.enums import ExternalEventStatus
from app.models.external_event_log import ExternalEventLog
from app.schemas.external_events import ExternalEventEnvelope
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_existing_event(
    session: AsyncSession,
    envelope: ExternalEventEnvelope,
) -> ExternalEventLog | None:
    result = await session.execute(
        select(ExternalEventLog).where(
            ExternalEventLog.source_system == envelope.source_system,
            ExternalEventLog.event_id == envelope.event_id,
        )
    )
    return result.scalar_one_or_none()


async def create_event_log(
    session: AsyncSession,
    envelope: ExternalEventEnvelope,
) -> ExternalEventLog:
    event_log = ExternalEventLog(
        source_system=envelope.source_system,
        event_id=envelope.event_id,
        event_type=envelope.event_type,
        schema_version=envelope.schema_version,
        occurred_at=envelope.occurred_at,
        received_at=datetime.now(timezone.utc),
        payload=envelope.payload,
        processed_status=ExternalEventStatus.pending,
        retry_count=0,
    )
    session.add(event_log)
    await session.flush()
    return event_log


def mark_processing(event_log: ExternalEventLog) -> None:
    event_log.processed_status = ExternalEventStatus.processing


def mark_success(
    event_log: ExternalEventLog,
    related_entity_type: str | None = None,
    related_entity_id: int | None = None,
) -> None:
    event_log.processed_status = ExternalEventStatus.success
    event_log.processed_at = datetime.now(timezone.utc)
    event_log.error_message = None
    event_log.related_entity_type = related_entity_type
    event_log.related_entity_id = related_entity_id


def mark_failed(event_log: ExternalEventLog, error: Exception | str) -> None:
    event_log.processed_status = ExternalEventStatus.failed
    event_log.processed_at = datetime.now(timezone.utc)
    event_log.error_message = str(error)
