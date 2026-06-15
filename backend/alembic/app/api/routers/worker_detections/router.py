from datetime import datetime
from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.user import User
from app.models.worker_detection import WorkerDetection
from app.schemas.worker_detections import (
    WorkerDetectionCreate,
    WorkerDetectionListResponse,
    WorkerDetectionResponse,
    WorkerDetectionUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/worker-detections", tags=["worker-detections"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_detection_or_404(det: WorkerDetection | None) -> WorkerDetection:
    if det is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작업자 감지 기록을 찾을 수 없습니다.",
        )
    return det


@router.post("", response_model=WorkerDetectionResponse, status_code=status.HTTP_201_CREATED)
async def create_worker_detection(
    body: WorkerDetectionCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> WorkerDetection:
    detection = WorkerDetection(**body.model_dump())
    session.add(detection)
    await session.commit()
    await session.refresh(detection)
    return detection


@router.get("", response_model=WorkerDetectionListResponse)
async def list_worker_detections(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    site_id: int | None = Query(default=None),
    camera_id: int | None = Query(default=None),
    process_id: int | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
) -> WorkerDetectionListResponse:
    conditions = []
    if site_id is not None:
        conditions.append(WorkerDetection.site_id == site_id)
    if camera_id is not None:
        conditions.append(WorkerDetection.camera_id == camera_id)
    if process_id is not None:
        conditions.append(WorkerDetection.process_id == process_id)
    if date_from is not None:
        conditions.append(WorkerDetection.entry_time >= date_from)
    if date_to is not None:
        conditions.append(WorkerDetection.entry_time <= date_to)

    total = (
        await session.execute(
            select(func.count()).select_from(WorkerDetection).where(*conditions)
        )
    ).scalar_one()

    offset = (page - 1) * size
    rows = (
        await session.execute(
            select(WorkerDetection)
            .where(*conditions)
            .order_by(WorkerDetection.entry_time.desc())
            .offset(offset)
            .limit(size)
        )
    ).scalars().all()

    return WorkerDetectionListResponse(
        items=[WorkerDetectionResponse.model_validate(d) for d in rows],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{detection_id}", response_model=WorkerDetectionResponse)
async def get_worker_detection(
    detection_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> WorkerDetection:
    result = await session.execute(
        select(WorkerDetection).where(WorkerDetection.id == detection_id)
    )
    return _get_detection_or_404(result.scalar_one_or_none())


@router.put("/{detection_id}", response_model=WorkerDetectionResponse)
async def update_worker_detection(
    detection_id: int,
    body: WorkerDetectionUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> WorkerDetection:
    result = await session.execute(
        select(WorkerDetection).where(WorkerDetection.id == detection_id)
    )
    detection = _get_detection_or_404(result.scalar_one_or_none())

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(detection, field, value)

    await session.commit()
    await session.refresh(detection)
    return detection
