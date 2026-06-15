from typing import Annotated

from app.api.deps import get_db_session
from app.models.camera import Camera
from app.models.nvr import NVR
from app.schemas.camera import CameraListResponse, CameraResponse
from app.schemas.nvr import NVRCreate, NVRListResponse, NVRResponse, NVRUpdate
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/nvrs", tags=["nvrs"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def _get_nvr_or_404(nvr: NVR | None) -> NVR:
    if nvr is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NVR을 찾을 수 없습니다.")
    return nvr


@router.post("", response_model=NVRResponse, status_code=status.HTTP_201_CREATED)
async def create_nvr(body: NVRCreate, session: DbSession) -> NVR:
    result = await session.execute(
        select(NVR).where(
            NVR.ip_address == str(body.ip_address),
            NVR.site_id == body.site_id,
            NVR.is_deleted.is_(False),
        )
    )
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="해당 사이트에 동일한 IP의 NVR이 이미 존재합니다.",
        )

    encrypted_password: str | None = None
    if body.password:
        from app.core.security import get_password_hash
        encrypted_password = get_password_hash(body.password)

    nvr = NVR(
        site_id=body.site_id,
        name=body.name,
        description=body.description,
        ip_address=str(body.ip_address),
        port=body.port,
        username=body.username,
        encrypted_password=encrypted_password,
        model_name=body.model_name,
        firmware_version=body.firmware_version,
        storage_capacity_gb=body.storage_capacity_gb,
        is_active=body.is_active,
    )
    session.add(nvr)
    await session.commit()
    await session.refresh(nvr)
    return nvr


@router.get("", response_model=NVRListResponse)
async def list_nvrs(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> NVRListResponse:
    base_where = NVR.is_deleted.is_(False)

    total_result = await session.execute(select(func.count()).select_from(NVR).where(base_where))
    total = total_result.scalar_one()

    offset = (page - 1) * size
    nvrs_result = await session.execute(
        select(NVR).where(base_where).order_by(NVR.id.asc()).offset(offset).limit(size)
    )
    nvrs = nvrs_result.scalars().all()

    return NVRListResponse(
        items=[NVRResponse.model_validate(nvr) for nvr in nvrs],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{nvr_id}", response_model=NVRResponse)
async def get_nvr(nvr_id: int, session: DbSession) -> NVR:
    result = await session.execute(
        select(NVR).where(NVR.id == nvr_id, NVR.is_deleted.is_(False))
    )
    return _get_nvr_or_404(result.scalar_one_or_none())


@router.put("/{nvr_id}", response_model=NVRResponse)
async def update_nvr(nvr_id: int, body: NVRUpdate, session: DbSession) -> NVR:
    result = await session.execute(
        select(NVR).where(NVR.id == nvr_id, NVR.is_deleted.is_(False))
    )
    nvr = _get_nvr_or_404(result.scalar_one_or_none())

    update_data = body.model_dump(exclude_none=True)

    if "password" in update_data:
        from app.core.security import get_password_hash
        nvr.encrypted_password = get_password_hash(update_data.pop("password"))
    else:
        update_data.pop("password", None)

    if "ip_address" in update_data:
        update_data["ip_address"] = str(update_data["ip_address"])

    for field, value in update_data.items():
        setattr(nvr, field, value)

    await session.commit()
    await session.refresh(nvr)
    return nvr


@router.delete("/{nvr_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nvr(nvr_id: int, session: DbSession) -> None:
    result = await session.execute(
        select(NVR).where(NVR.id == nvr_id, NVR.is_deleted.is_(False))
    )
    nvr = _get_nvr_or_404(result.scalar_one_or_none())
    nvr.is_deleted = True
    await session.commit()


@router.get("/{nvr_id}/cameras", response_model=CameraListResponse, tags=["cameras"])
async def list_cameras_by_nvr(
    nvr_id: int,
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> CameraListResponse:
    nvr_result = await session.execute(
        select(NVR).where(NVR.id == nvr_id, NVR.is_deleted.is_(False))
    )
    _get_nvr_or_404(nvr_result.scalar_one_or_none())

    base_where = (Camera.nvr_id == nvr_id, Camera.is_deleted.is_(False))

    total_result = await session.execute(
        select(func.count()).select_from(Camera).where(*base_where)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    cameras_result = await session.execute(
        select(Camera).where(*base_where).order_by(Camera.id.asc()).offset(offset).limit(size)
    )
    cameras = cameras_result.scalars().all()

    return CameraListResponse(
        items=[CameraResponse.model_validate(c) for c in cameras],
        total=total,
        page=page,
        size=size,
    )
