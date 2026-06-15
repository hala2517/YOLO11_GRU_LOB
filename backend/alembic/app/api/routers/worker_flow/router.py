import datetime as dt
from typing import Annotated, Any

from app.api.deps import get_current_user, get_db_session
from app.models.efficiency_metric import EfficiencyMetric
from app.models.enums import MesSyncStatus, ShiftType
from app.models.mes_sync_log import MesSyncLog
from app.models.process import Process
from app.models.process_flow import ProcessFlow
from app.models.user import User
from app.models.worker_detection import WorkerDetection
from app.schemas.efficiency_metrics import EfficiencyMetricResponse
from app.schemas.process_flows import ProcessFlowResponse
from app.schemas.processes import ProcessResponse
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/worker-flow", tags=["worker-flow"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/dashboard", response_model=dict[str, Any])
async def get_worker_flow_dashboard(
    session: DbSession,
    current_user: CurrentUser,
    site_id: int | None = Query(default=None),
    date: dt.date | None = Query(default=None),
    shift: ShiftType | None = Query(default=None),
) -> dict[str, Any]:
    target_date = date or dt.date.today()

    process_conditions = [Process.is_deleted.is_(False), Process.is_active.is_(True)]
    if site_id is not None:
        process_conditions.append(Process.site_id == site_id)

    processes_result = await session.execute(
        select(Process)
        .where(*process_conditions)
        .order_by(Process.line_order.asc(), Process.id.asc())
    )
    processes = processes_result.scalars().all()
    process_ids = [p.id for p in processes]

    active_flows: list[dict[str, Any]] = []
    if process_ids:
        flows_result = await session.execute(
            select(ProcessFlow).where(
                ProcessFlow.process_id.in_(process_ids),
                ProcessFlow.is_active.is_(True),
                ProcessFlow.is_deleted.is_(False),
            )
        )
        flows = flows_result.scalars().all()
        active_flows = [ProcessFlowResponse.model_validate(f).model_dump() for f in flows]

    metric_conditions = [
        EfficiencyMetric.date == target_date,
    ]
    if process_ids:
        metric_conditions.append(EfficiencyMetric.process_id.in_(process_ids))
    if shift is not None:
        metric_conditions.append(EfficiencyMetric.shift == shift)

    metrics_result = await session.execute(
        select(EfficiencyMetric)
        .where(*metric_conditions)
        .order_by(EfficiencyMetric.process_id.asc(), EfficiencyMetric.shift.asc())
    )
    metrics = metrics_result.scalars().all()

    detection_conditions = [
        WorkerDetection.entry_time >= dt.datetime.combine(target_date, dt.time.min),
        WorkerDetection.entry_time < dt.datetime.combine(
            target_date + dt.timedelta(days=1), dt.time.min
        ),
    ]
    if site_id is not None:
        detection_conditions.append(WorkerDetection.site_id == site_id)

    detections_count_result = await session.execute(
        select(
            WorkerDetection.process_id,
            func.count(WorkerDetection.id).label("cnt"),
            func.avg(WorkerDetection.duration_seconds).label("avg_duration"),
        )
        .where(*detection_conditions)
        .group_by(WorkerDetection.process_id)
    )
    detection_stats = {
        row.process_id: {
            "worker_count_today": row.cnt,
            "avg_duration_seconds": float(row.avg_duration) if row.avg_duration else None,
        }
        for row in detections_count_result.all()
    }

    mes_conditions = [MesSyncLog.processed_status == MesSyncStatus.pending]
    if site_id is not None:
        mes_conditions.append(MesSyncLog.site_id == site_id)
    pending_mes_result = await session.execute(
        select(func.count()).select_from(MesSyncLog).where(*mes_conditions)
    )
    pending_mes_count = pending_mes_result.scalar_one()

    process_summary = []
    for p in processes:
        process_metrics = [m for m in metrics if m.process_id == p.id]
        det_stat = detection_stats.get(p.id, {})
        process_summary.append({
            "process": ProcessResponse.model_validate(p).model_dump(),
            "efficiency_metrics": [
                EfficiencyMetricResponse.model_validate(m).model_dump()
                for m in process_metrics
            ],
            "worker_count_today": det_stat.get("worker_count_today", 0),
            "avg_duration_seconds": det_stat.get("avg_duration_seconds"),
        })

    return {
        "site_id": site_id,
        "date": target_date,
        "shift": shift,
        "process_summary": process_summary,
        "active_process_flows": active_flows,
        "pending_mes_sync_count": pending_mes_count,
        "generated_at": dt.datetime.now(dt.timezone.utc),
    }
