import datetime as dt
from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.standard_process_chart import StandardProcessChart
from app.models.user import User
from app.schemas.line_productivity import (
    LineProductivityItem,
    LineProductivityListResponse,
)
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/line-productivity", tags=["line-productivity"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=LineProductivityListResponse)
async def list_line_productivity(
    session: DbSession,
    current_user: CurrentUser,
    work_date: dt.date | None = Query(default=None),
    line_code: str | None = Query(default=None),
    product_code: str | None = Query(default=None),
) -> LineProductivityListResponse:
    conditions = [StandardProcessChart.is_deleted.is_(False)]
    if line_code is not None:
        conditions.append(StandardProcessChart.line_code == line_code)
    if product_code is not None:
        conditions.append(StandardProcessChart.product_code == product_code)

    rows = (
        await session.execute(
            select(
                StandardProcessChart.line_code,
                StandardProcessChart.product_code,
                func.max(StandardProcessChart.product_name).label("product_name"),
                func.count(StandardProcessChart.id).label("chart_count"),
            )
            .where(*conditions)
            .group_by(StandardProcessChart.line_code, StandardProcessChart.product_code)
            .order_by(StandardProcessChart.line_code.asc(), StandardProcessChart.product_code.asc())
        )
    ).all()

    items = [
        LineProductivityItem(
            line_code=row.line_code,
            product_code=row.product_code,
            product_name=row.product_name,
            standard_process_chart_count=row.chart_count,
            note="MES 생산성 지표 연동 전: 표준공정도 보유 라인만 표시",
        )
        for row in rows
    ]

    return LineProductivityListResponse(
        items=items,
        total=len(items),
        work_date=work_date,
        data_source="standard_process_charts_only",
        message=(
            "생산량/가동시간/불량률/인력 투입/납기 등 생산성 값은 "
            "MES Adapter 연동 후 조합되어 내려갑니다."
        ),
    )
