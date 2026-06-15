from datetime import datetime, timezone
from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.enums import RecognitionType
from app.models.recognition_log import RecognitionLog
from app.models.user import User
from app.schemas.recognition_logs import (
    RecognitionLogBulkCreate,
    RecognitionLogCreate,
    RecognitionLogListResponse,
    RecognitionLogResponse,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/recognition-logs", tags=["recognition-logs"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_log_or_404(log: RecognitionLog | None) -> RecognitionLog:
    if log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="인식 로그를 찾을 수 없습니다.",
        )
    return log


@router.post(
    "",
    response_model=list[RecognitionLogResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_recognition_logs(
    body: RecognitionLogBulkCreate | RecognitionLogCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> list[RecognitionLog]:
    if isinstance(body, RecognitionLogCreate):
        items = [body]
    else:
        items = body.items

    now = datetime.now(timezone.utc)
    created: list[RecognitionLog] = []
    for item in items:
        data = item.model_dump()
        metadata = data.pop("metadata_", None)
        log = RecognitionLog(**data, metadata_=metadata, created_at=now)
        session.add(log)
        created.append(log)

    await session.commit()
    for log in created:
        await session.refresh(log)

    return created


@router.get("", response_model=RecognitionLogListResponse)
async def list_recognition_logs(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    site_id: int | None = Query(default=None),
    camera_id: int | None = Query(default=None),
    recognition_type: RecognitionType | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
) -> RecognitionLogListResponse:
    conditions = []
    if site_id is not None:
        conditions.append(RecognitionLog.site_id == site_id)
    if camera_id is not None:
        conditions.append(RecognitionLog.camera_id == camera_id)
    if recognition_type is not None:
        conditions.append(RecognitionLog.recognition_type == recognition_type)
    if date_from is not None:
        conditions.append(RecognitionLog.detected_at >= date_from)
    if date_to is not None:
        conditions.append(RecognitionLog.detected_at <= date_to)

    total_result = await session.execute(
        select(func.count()).select_from(RecognitionLog).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(RecognitionLog)
        .where(*conditions)
        .order_by(RecognitionLog.detected_at.desc())
        .offset(offset)
        .limit(size)
    )
    logs = result.scalars().all()

    return RecognitionLogListResponse(
        items=[RecognitionLogResponse.model_validate(l) for l in logs],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{log_id}", response_model=RecognitionLogResponse)
async def get_recognition_log(
    log_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> RecognitionLog:
    result = await session.execute(
        select(RecognitionLog).where(RecognitionLog.id == log_id)
    )
    return _get_log_or_404(result.scalar_one_or_none())
