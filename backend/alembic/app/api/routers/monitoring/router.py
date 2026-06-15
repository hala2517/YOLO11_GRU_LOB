from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from app.api.deps import get_current_user, get_db_session
from app.models.alert import AlertLog
from app.models.camera import Camera
from app.models.enums import DataCollectionJobStatus, DeviceStatus
from app.models.data_collection_job import DataCollectionJob
from app.models.recognition_log import RecognitionLog
from app.models.user import User
from app.schemas.recognition_logs import RecognitionLogResponse
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/dashboard", response_model=dict[str, Any])
async def get_monitoring_dashboard(
    session: DbSession,
    current_user: CurrentUser,
    site_id: int | None = None,
) -> dict[str, Any]:
    camera_conditions = [Camera.is_deleted.is_(False)]
    if site_id is not None:
        camera_conditions.append(Camera.site_id == site_id)

    camera_result = await session.execute(
        select(Camera.status, func.count(Camera.id).label("cnt"))
        .where(*camera_conditions)
        .group_by(Camera.status)
    )
    camera_status_rows = camera_result.all()
    camera_summary: dict[str, int] = {
        "total": 0,
        "online": 0,
        "offline": 0,
        "error": 0,
        "maintenance": 0,
    }
    for row in camera_status_rows:
        camera_summary[row.status.value] = row.cnt
        camera_summary["total"] += row.cnt

    since_24h = datetime.now(timezone.utc) - timedelta(hours=24)

    alert_conditions = [AlertLog.detected_at >= since_24h]
    if site_id is not None:
        alert_conditions.append(AlertLog.site_id == site_id)

    alert_result = await session.execute(
        select(AlertLog)
        .where(*alert_conditions)
        .order_by(AlertLog.detected_at.desc())
        .limit(10)
    )
    recent_alerts = alert_result.scalars().all()
    alert_list = [
        {
            "id": a.id,
            "site_id": a.site_id,
            "camera_id": a.camera_id,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "title": a.title,
            "detected_at": a.detected_at,
            "is_acknowledged": a.is_acknowledged,
        }
        for a in recent_alerts
    ]

    recog_conditions = [RecognitionLog.detected_at >= since_24h]
    if site_id is not None:
        recog_conditions.append(RecognitionLog.site_id == site_id)

    recog_result = await session.execute(
        select(RecognitionLog)
        .where(*recog_conditions)
        .order_by(RecognitionLog.detected_at.desc())
        .limit(10)
    )
    recent_recognitions = [
        RecognitionLogResponse.model_validate(r) for r in recog_result.scalars().all()
    ]

    job_conditions = [
        DataCollectionJob.is_deleted.is_(False),
        DataCollectionJob.status == DataCollectionJobStatus.running,
    ]
    active_jobs_result = await session.execute(
        select(func.count()).select_from(DataCollectionJob).where(*job_conditions)
    )
    active_jobs_count = active_jobs_result.scalar_one()

    unack_conditions = [AlertLog.is_acknowledged.is_(False)]
    if site_id is not None:
        unack_conditions.append(AlertLog.site_id == site_id)
    unack_result = await session.execute(
        select(func.count()).select_from(AlertLog).where(*unack_conditions)
    )
    unacknowledged_alerts = unack_result.scalar_one()

    return {
        "camera_summary": camera_summary,
        "recent_alerts": alert_list,
        "recent_recognitions": [r.model_dump() for r in recent_recognitions],
        "active_data_collection_jobs": active_jobs_count,
        "unacknowledged_alerts": unacknowledged_alerts,
        "generated_at": datetime.now(timezone.utc),
    }
