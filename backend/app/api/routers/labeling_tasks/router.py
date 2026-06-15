from datetime import datetime, timezone
from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.enums import LabelingTaskStatus
from app.models.labeling_task import LabelingTask
from app.models.user import User
from app.schemas.labeling_tasks import (
    LabelingTaskCreate,
    LabelingTaskListResponse,
    LabelingTaskResponse,
    LabelingTaskUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/labeling-tasks", tags=["labeling-tasks"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_task_or_404(task: LabelingTask | None) -> LabelingTask:
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="라벨링 작업을 찾을 수 없습니다.",
        )
    return task


@router.post("", response_model=LabelingTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_labeling_task(
    body: LabelingTaskCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> LabelingTask:
    task = LabelingTask(**body.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.get("", response_model=LabelingTaskListResponse)
async def list_labeling_tasks(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    dataset_id: int | None = Query(default=None),
    status_filter: LabelingTaskStatus | None = Query(default=None, alias="status"),
) -> LabelingTaskListResponse:
    conditions = [LabelingTask.is_deleted.is_(False)]
    if dataset_id is not None:
        conditions.append(LabelingTask.dataset_id == dataset_id)
    if status_filter is not None:
        conditions.append(LabelingTask.status == status_filter)

    total_result = await session.execute(
        select(func.count()).select_from(LabelingTask).where(*conditions)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    result = await session.execute(
        select(LabelingTask)
        .where(*conditions)
        .order_by(LabelingTask.id.desc())
        .offset(offset)
        .limit(size)
    )
    tasks = result.scalars().all()

    return LabelingTaskListResponse(
        items=[LabelingTaskResponse.model_validate(t) for t in tasks],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{task_id}", response_model=LabelingTaskResponse)
async def get_labeling_task(
    task_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> LabelingTask:
    result = await session.execute(
        select(LabelingTask).where(
            LabelingTask.id == task_id,
            LabelingTask.is_deleted.is_(False),
        )
    )
    return _get_task_or_404(result.scalar_one_or_none())


@router.put("/{task_id}", response_model=LabelingTaskResponse)
async def update_labeling_task(
    task_id: int,
    body: LabelingTaskUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> LabelingTask:
    result = await session.execute(
        select(LabelingTask).where(
            LabelingTask.id == task_id,
            LabelingTask.is_deleted.is_(False),
        )
    )
    task = _get_task_or_404(result.scalar_one_or_none())

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await session.commit()
    await session.refresh(task)
    return task


@router.post("/{task_id}/complete", response_model=LabelingTaskResponse)
async def complete_labeling_task(
    task_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> LabelingTask:
    result = await session.execute(
        select(LabelingTask).where(
            LabelingTask.id == task_id,
            LabelingTask.is_deleted.is_(False),
        )
    )
    task = _get_task_or_404(result.scalar_one_or_none())

    if task.status == LabelingTaskStatus.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 완료된 작업입니다.",
        )

    task.status = LabelingTaskStatus.completed
    task.progress = 100
    task.completed_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(task)
    return task
