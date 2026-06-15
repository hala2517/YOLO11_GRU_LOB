from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from app.models.alert import AlertLog
from app.models.camera import Camera
from app.models.enums import AlertSeverity, AlertType, RecognitionType
from app.models.recognition_log import RecognitionLog
from app.schemas.external_events import ExternalEventEnvelope
from app.services.external_event_log_service import (
    create_event_log,
    get_existing_event,
    mark_failed,
    mark_processing,
    mark_success,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


def _decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value))


def _datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise ValueError("유효한 datetime 값이 아닙니다.")


async def _find_camera(session: AsyncSession, payload: dict[str, Any]) -> Camera | None:
    camera_id = payload.get("camera_id")
    if camera_id is not None:
        result = await session.execute(
            select(Camera).where(Camera.id == camera_id, Camera.is_deleted.is_(False))
        )
        return result.scalar_one_or_none()

    camera_code = payload.get("camera_code")
    if camera_code:
        result = await session.execute(
            select(Camera).where(Camera.camera_code == camera_code, Camera.is_deleted.is_(False))
        )
        return result.scalar_one_or_none()
    return None


def _alert_type_for(payload: dict[str, Any]) -> AlertType | None:
    recognition_type = payload.get("recognition_type")
    class_name = str(payload.get("class_name") or "").lower()
    if recognition_type == RecognitionType.intrusion.value:
        return AlertType.intrusion
    if "unauthorized" in class_name or "비인가" in class_name:
        return AlertType.unauthorized_person
    if recognition_type == RecognitionType.helmet.value and payload.get("policy_violation"):
        return AlertType.helmet_color
    return None


async def process_recognition_event(
    session: AsyncSession,
    envelope: ExternalEventEnvelope,
):
    existing = await get_existing_event(session, envelope)
    if existing is not None:
        return existing

    event_log = await create_event_log(session, envelope)
    mark_processing(event_log)

    try:
        payload = envelope.payload
        camera = await _find_camera(session, payload)
        if camera is None:
            raise ValueError("인식 이벤트와 연결할 Camera를 찾을 수 없습니다.")

        recognition_type = RecognitionType(payload["recognition_type"])
        detected_at = _datetime(payload.get("detected_at") or envelope.occurred_at)
        position = payload.get("position") or {}
        log = RecognitionLog(
            site_id=camera.site_id,
            camera_id=camera.id,
            labeling_task_id=payload.get("labeling_task_id"),
            recognition_type=recognition_type,
            class_name=payload["class_name"],
            confidence=_decimal(payload.get("confidence")),
            bbox=payload.get("bbox"),
            position_x=_decimal(position.get("x") or payload.get("position_x")),
            position_y=_decimal(position.get("y") or payload.get("position_y")),
            detected_at=detected_at,
            metadata_=payload.get("metadata"),
            created_at=datetime.now(timezone.utc),
        )
        session.add(log)
        await session.flush()

        alert_type = _alert_type_for(payload)
        if alert_type is not None:
            now = datetime.now(timezone.utc)
            session.add(
                AlertLog(
                    site_id=camera.site_id,
                    camera_id=camera.id,
                    threshold_id=None,
                    alert_type=alert_type,
                    severity=AlertSeverity(payload.get("severity", AlertSeverity.medium.value)),
                    title=payload.get("alert_title") or "AI 인식 이벤트 알림",
                    message=payload.get("alert_message")
                    or f"{log.class_name} 이벤트가 감지되었습니다.",
                    detected_at=detected_at,
                    position_x=log.position_x,
                    position_y=log.position_y,
                    metadata_={
                        "external_event_id": envelope.event_id,
                        "recognition_log_id": log.id,
                    },
                    created_at=now,
                )
            )

        mark_success(event_log, "recognition_logs", log.id)
    except Exception as exc:
        mark_failed(event_log, exc)

    await session.commit()
    await session.refresh(event_log)
    return event_log
