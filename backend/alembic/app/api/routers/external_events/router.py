from typing import Annotated

from app.api.deps import get_db_session
from app.models.enums import ExternalEventStatus
from app.models.external_event_log import ExternalEventLog
from app.schemas.external_events import ExternalEventLogResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/external-events", tags=["external-events"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("", response_model=dict)
async def list_external_events(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    source_system: str | None = Query(default=None),
    event_type: str | None = Query(default=None),
    processed_status: ExternalEventStatus | None = Query(default=None),
) -> dict:
    conditions = []
    if source_system is not None:
        conditions.append(ExternalEventLog.source_system == source_system)
    if event_type is not None:
        conditions.append(ExternalEventLog.event_type == event_type)
    if processed_status is not None:
        conditions.append(ExternalEventLog.processed_status == processed_status)

    total = (
        await session.execute(
            select(func.count()).select_from(ExternalEventLog).where(*conditions)
        )
    ).scalar_one()
    rows = (
        await session.execute(
            select(ExternalEventLog)
            .where(*conditions)
            .order_by(ExternalEventLog.received_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
    ).scalars().all()

    return {
        "items": [ExternalEventLogResponse.model_validate(row).model_dump() for row in rows],
        "total": total,
        "page": page,
        "size": size,
    }


@router.get("/{event_log_id}", response_model=ExternalEventLogResponse)
async def get_external_event(
    event_log_id: int,
    session: DbSession,
) -> ExternalEventLog:
    result = await session.execute(
        select(ExternalEventLog).where(ExternalEventLog.id == event_log_id)
    )
    event_log = result.scalar_one_or_none()
    if event_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="외부 이벤트 로그를 찾을 수 없습니다.",
        )
    return event_log
