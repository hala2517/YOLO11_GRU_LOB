from datetime import datetime
from typing import Annotated, Any

from app.api.deps import get_current_user, get_db_session
from app.models.collected_video import CollectedVideo
from app.models.enums import CollectedVideoStatus
from app.models.user import User
from app.schemas.collected_videos import (
    CollectedVideoCreate,
    CollectedVideoListResponse,
    CollectedVideoResponse,
    CollectedVideoUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/collected-videos", tags=["collected-videos"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_video_or_404(video: CollectedVideo | None) -> CollectedVideo:
    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="수집 영상을 찾을 수 없습니다.",
        )
    return video


@router.post("", response_model=CollectedVideoResponse, status_code=status.HTTP_201_CREATED)
async def create_collected_video(
    body: CollectedVideoCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> CollectedVideo:
    video = CollectedVideo(**body.model_dump())
    session.add(video)
    await session.commit()
    await session.refresh(video)
    return video


@router.get("", response_model=CollectedVideoListResponse)
async def list_collected_videos(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    camera_id: int | None = Query(default=None),
    site_id: int | None = Query(default=None),
    data_collection_job_id: int | None = Query(default=None),
    status_filter: CollectedVideoStatus | None = Query(default=None, alias="status"),
    recorded_from: datetime | None = Query(default=None),
    recorded_to: datetime | None = Query(default=None),
) -> CollectedVideoListResponse:
    conditions = [CollectedVideo.is_deleted.is_(False)]
    if camera_id is not None:
        conditions.append(CollectedVideo.camera_id == camera_id)
    if site_id is not None:
        conditions.append(CollectedVideo.site_id == site_id)
    if data_collection_job_id is not None:
        conditions.append(CollectedVideo.data_collection_job_id == data_collection_job_id)
    if status_filter is not None:
        conditions.append(CollectedVideo.status == status_filter)
    if recorded_from is not None:
        conditions.append(CollectedVideo.recorded_at >= recorded_from)
    if recorded_to is not None:
        conditions.append(CollectedVideo.recorded_at <= recorded_to)

    total = (
        await session.execute(
            select(func.count()).select_from(CollectedVideo).where(*conditions)
        )
    ).scalar_one()

    offset = (page - 1) * size
    rows = (
        await session.execute(
            select(CollectedVideo)
            .where(*conditions)
            .order_by(CollectedVideo.recorded_at.desc())
            .offset(offset)
            .limit(size)
        )
    ).scalars().all()

    return CollectedVideoListResponse(
        items=[CollectedVideoResponse.model_validate(v) for v in rows],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{video_id}", response_model=CollectedVideoResponse)
async def get_collected_video(
    video_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> CollectedVideo:
    result = await session.execute(
        select(CollectedVideo).where(
            CollectedVideo.id == video_id,
            CollectedVideo.is_deleted.is_(False),
        )
    )
    return _get_video_or_404(result.scalar_one_or_none())


@router.put("/{video_id}", response_model=CollectedVideoResponse)
async def update_collected_video(
    video_id: int,
    body: CollectedVideoUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> CollectedVideo:
    result = await session.execute(
        select(CollectedVideo).where(
            CollectedVideo.id == video_id,
            CollectedVideo.is_deleted.is_(False),
        )
    )
    video = _get_video_or_404(result.scalar_one_or_none())

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(video, field, value)

    await session.commit()
    await session.refresh(video)
    return video


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collected_video(
    video_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> None:
    result = await session.execute(
        select(CollectedVideo).where(
            CollectedVideo.id == video_id,
            CollectedVideo.is_deleted.is_(False),
        )
    )
    video = _get_video_or_404(result.scalar_one_or_none())
    video.is_deleted = True
    await session.commit()


@router.get("/{video_id}/url", response_model=dict[str, Any])
async def get_collected_video_url(
    video_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> dict[str, Any]:
    result = await session.execute(
        select(CollectedVideo).where(
            CollectedVideo.id == video_id,
            CollectedVideo.is_deleted.is_(False),
        )
    )
    video = _get_video_or_404(result.scalar_one_or_none())

    if video.storage_type == "s3":
        url = f"/api/v1/media/s3/{video.file_path}"
    else:
        url = f"/api/v1/media/local/{video.file_path}"

    return {
        "video_id": video.id,
        "file_name": video.file_name,
        "storage_type": video.storage_type,
        "url": url,
        "duration_seconds": video.duration_seconds,
    }
