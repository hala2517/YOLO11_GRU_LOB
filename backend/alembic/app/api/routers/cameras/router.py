from typing import Annotated, Any

from app.api.deps import get_current_user, get_db_session
from app.core.config import get_settings
from app.models.camera import Camera
from app.models.nvr import NVR
from app.models.user import User
from app.schemas.camera import CameraCreate, CameraListResponse, CameraResponse, CameraUpdate
from app.schemas.external_events import CameraStreamResponse
from app.services.cctv_streaming_service import (
    build_playback_url,
    create_or_touch_stream_session,
    create_stream_token,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cameras", tags=["cameras"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _get_camera_or_404(camera: Camera | None) -> Camera:
    if camera is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="카메라를 찾을 수 없습니다.",
        )
    return camera


@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
async def create_camera(body: CameraCreate, session: DbSession) -> Camera:
    nvr_result = await session.execute(
        select(NVR).where(NVR.id == body.nvr_id, NVR.is_deleted.is_(False))
    )
    nvr = nvr_result.scalar_one_or_none()
    if nvr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NVR을 찾을 수 없습니다.",
        )

    if body.camera_code:
        dup_result = await session.execute(
            select(Camera).where(
                Camera.camera_code == body.camera_code,
                Camera.is_deleted.is_(False),
            )
        )
        if dup_result.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 카메라 코드입니다.",
            )

    camera = Camera(
        nvr_id=body.nvr_id,
        site_id=nvr.site_id,
        name=body.name,
        camera_code=body.camera_code,
        channel=body.channel,
        rtsp_url=body.rtsp_url,
        location=body.location,
        position_x=body.position_x,
        position_y=body.position_y,
        resolution=body.resolution,
        fps=body.fps,
        model_name=body.model_name,
        is_active=body.is_active,
    )
    session.add(camera)
    await session.commit()
    await session.refresh(camera)
    return camera


@router.get("", response_model=CameraListResponse)
async def list_cameras(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> CameraListResponse:
    base_where = Camera.is_deleted.is_(False)

    total_result = await session.execute(
        select(func.count()).select_from(Camera).where(base_where)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    cameras_result = await session.execute(
        select(Camera).where(base_where).order_by(Camera.id.asc()).offset(offset).limit(size)
    )
    cameras = cameras_result.scalars().all()

    return CameraListResponse(
        items=[CameraResponse.model_validate(c) for c in cameras],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(camera_id: int, session: DbSession) -> Camera:
    result = await session.execute(
        select(Camera).where(Camera.id == camera_id, Camera.is_deleted.is_(False))
    )
    return _get_camera_or_404(result.scalar_one_or_none())


@router.put("/{camera_id}", response_model=CameraResponse)
async def update_camera(camera_id: int, body: CameraUpdate, session: DbSession) -> Camera:
    result = await session.execute(
        select(Camera).where(Camera.id == camera_id, Camera.is_deleted.is_(False))
    )
    camera = _get_camera_or_404(result.scalar_one_or_none())

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(camera, field, value)

    await session.commit()
    await session.refresh(camera)
    return camera


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(camera_id: int, session: DbSession) -> None:
    result = await session.execute(
        select(Camera).where(Camera.id == camera_id, Camera.is_deleted.is_(False))
    )
    camera = _get_camera_or_404(result.scalar_one_or_none())
    camera.is_deleted = True
    await session.commit()


@router.get("/{camera_id}/status", response_model=dict[str, Any])
async def get_camera_status(
    camera_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> dict[str, Any]:
    result = await session.execute(
        select(Camera).where(Camera.id == camera_id, Camera.is_deleted.is_(False))
    )
    camera = _get_camera_or_404(result.scalar_one_or_none())
    return {
        "camera_id": camera.id,
        "name": camera.name,
        "status": camera.status,
        "is_active": camera.is_active,
        "last_connected_at": camera.last_connected_at,
        "resolution": camera.resolution,
        "fps": camera.fps,
    }


@router.get("/{camera_id}/stream", response_model=CameraStreamResponse)
async def get_camera_stream(
    camera_id: int,
    session: DbSession,
    current_user: CurrentUser,
) -> CameraStreamResponse:
    result = await session.execute(
        select(Camera).where(Camera.id == camera_id, Camera.is_deleted.is_(False))
    )
    camera = _get_camera_or_404(result.scalar_one_or_none())

    if not camera.rtsp_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="이 카메라에 등록된 스트림 URL이 없습니다.",
        )

    token, expires_at = create_stream_token(camera.id)
    playback_url, path = build_playback_url(camera, token)
    stream_type = get_settings().cctv_stream_mode
    await create_or_touch_stream_session(session, camera, playback_url, path, stream_type)
    await session.commit()

    return CameraStreamResponse(
        camera_id=camera.id,
        name=camera.name,
        stream_type=stream_type,
        playback_url=playback_url,
        path=path,
        expires_at=expires_at,
        status=camera.status.value,
    )
