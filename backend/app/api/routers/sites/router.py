from typing import Annotated

from app.api.deps import get_db_session
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteListResponse, SiteResponse, SiteUpdate
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/sites", tags=["sites"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def _get_site_or_404(site: Site | None) -> Site:
    if site is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="현장을 찾을 수 없습니다.",
        )
    return site


@router.post("", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
async def create_site(body: SiteCreate, session: DbSession) -> Site:
    dup_result = await session.execute(
        select(Site).where(Site.name == body.name, Site.is_deleted.is_(False))
    )
    if dup_result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 현장 이름입니다.",
        )

    site = Site(**body.model_dump())
    session.add(site)
    await session.commit()
    await session.refresh(site)
    return site


@router.get("", response_model=SiteListResponse)
async def list_sites(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> SiteListResponse:
    base_where = Site.is_deleted.is_(False)

    total_result = await session.execute(
        select(func.count()).select_from(Site).where(base_where)
    )
    total = total_result.scalar_one()

    offset = (page - 1) * size
    sites_result = await session.execute(
        select(Site).where(base_where).order_by(Site.id.asc()).offset(offset).limit(size)
    )
    sites = sites_result.scalars().all()

    return SiteListResponse(
        items=[SiteResponse.model_validate(s) for s in sites],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(site_id: int, session: DbSession) -> Site:
    result = await session.execute(
        select(Site).where(Site.id == site_id, Site.is_deleted.is_(False))
    )
    return _get_site_or_404(result.scalar_one_or_none())


@router.put("/{site_id}", response_model=SiteResponse)
async def update_site(site_id: int, body: SiteUpdate, session: DbSession) -> Site:
    result = await session.execute(
        select(Site).where(Site.id == site_id, Site.is_deleted.is_(False))
    )
    site = _get_site_or_404(result.scalar_one_or_none())

    update_data = body.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(site, field, value)

    await session.commit()
    await session.refresh(site)
    return site


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(site_id: int, session: DbSession) -> None:
    result = await session.execute(
        select(Site).where(Site.id == site_id, Site.is_deleted.is_(False))
    )
    site = _get_site_or_404(result.scalar_one_or_none())
    site.is_deleted = True
    await session.commit()
