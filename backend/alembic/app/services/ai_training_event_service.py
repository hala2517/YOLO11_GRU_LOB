from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from app.models.ai_model import AIModel
from app.models.enums import AIModelType, ExternalEventStatus, TrainingJobStatus
from app.models.evaluation_result import EvaluationResult
from app.models.training_job import TrainingJob
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


async def _find_training_job(session: AsyncSession, payload: dict[str, Any]) -> TrainingJob | None:
    job_id = payload.get("training_job_id")
    if job_id is not None:
        result = await session.execute(select(TrainingJob).where(TrainingJob.id == job_id))
        return result.scalar_one_or_none()

    external_job_id = payload.get("external_job_id")
    if external_job_id:
        result = await session.execute(
            select(TrainingJob).where(TrainingJob.external_job_id == external_job_id)
        )
        return result.scalar_one_or_none()
    return None


async def _create_or_update_model(
    session: AsyncSession,
    model_payload: dict[str, Any],
    metrics: dict[str, Any],
) -> AIModel | None:
    if not model_payload:
        return None

    name = model_payload.get("name")
    version = model_payload.get("version")
    model_type = model_payload.get("model_type", AIModelType.detection.value)
    if not name or not version:
        return None

    result = await session.execute(
        select(AIModel).where(AIModel.name == name, AIModel.version == version)
    )
    model = result.scalar_one_or_none()
    if model is None:
        model = AIModel(name=name, version=version, model_type=AIModelType(model_type))
        session.add(model)

    model.file_path = model_payload.get("artifact_uri") or model_payload.get("file_path")
    model.file_size_bytes = model_payload.get("file_size_bytes")
    model.mAP = _decimal(metrics.get("mAP"))
    model.precision = _decimal(metrics.get("precision"))
    model.recall = _decimal(metrics.get("recall"))
    model.trained_at = datetime.now(timezone.utc)
    model.is_active = True
    return model


async def process_training_event(
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
        job = await _find_training_job(session, payload)
        if job is None:
            raise ValueError("학습 이벤트와 연결할 TrainingJob을 찾을 수 없습니다.")

        job.source_system = envelope.source_system
        job.external_job_id = payload.get("external_job_id") or job.external_job_id
        raw_events = list(job.raw_events or [])
        raw_events.append(
            {
                "event_id": envelope.event_id,
                "event_type": envelope.event_type,
                "occurred_at": envelope.occurred_at.isoformat(),
                "payload": envelope.payload,
            }
        )
        job.raw_events = raw_events

        metrics = payload.get("metrics") or {}
        if metrics:
            job.metrics = metrics

        if envelope.event_type == "training.started":
            job.status = TrainingJobStatus.running
            job.started_at = job.started_at or datetime.now(timezone.utc)
        elif envelope.event_type == "training.progress":
            job.status = TrainingJobStatus.running
            job.progress = int(payload.get("progress", job.progress or 0))
        elif envelope.event_type == "training.completed":
            job.status = TrainingJobStatus.completed
            job.progress = 100
            job.completed_at = datetime.now(timezone.utc)
            model = await _create_or_update_model(session, payload.get("model") or {}, metrics)
            if model is not None:
                await session.flush()
                job.model_id = model.id
                session.add(
                    EvaluationResult(
                        model_id=model.id,
                        dataset_id=job.dataset_id,
                        training_job_id=job.id,
                        evaluation_date=datetime.now(timezone.utc),
                        mAP=_decimal(metrics.get("mAP")),
                        precision=_decimal(metrics.get("precision")),
                        recall=_decimal(metrics.get("recall")),
                        f1_score=_decimal(metrics.get("f1_score")),
                        inference_time_ms=metrics.get("inference_time_ms"),
                        accuracy=_decimal(metrics.get("accuracy")),
                        source_file_path=(payload.get("model") or {}).get("artifact_uri")
                        or f"external:{envelope.event_id}",
                        file_hash=payload.get("file_hash"),
                        raw_metrics=metrics,
                        notes=f"Imported from {envelope.source_system}",
                        is_processed=True,
                    )
                )
        elif envelope.event_type == "training.failed":
            job.status = TrainingJobStatus.failed
            job.error_message = payload.get("error_message") or payload.get("error")
            job.completed_at = datetime.now(timezone.utc)
        elif envelope.event_type == "evaluation.completed":
            if job.model_id is None:
                raise ValueError("평가 결과를 연결할 AIModel이 없습니다.")
            session.add(
                EvaluationResult(
                    model_id=job.model_id,
                    dataset_id=job.dataset_id,
                    training_job_id=job.id,
                    evaluation_date=datetime.now(timezone.utc),
                    mAP=_decimal(metrics.get("mAP")),
                    precision=_decimal(metrics.get("precision")),
                    recall=_decimal(metrics.get("recall")),
                    f1_score=_decimal(metrics.get("f1_score")),
                    inference_time_ms=metrics.get("inference_time_ms"),
                    accuracy=_decimal(metrics.get("accuracy")),
                    source_file_path=payload.get("source_file_path") or f"external:{envelope.event_id}",
                    file_hash=payload.get("file_hash"),
                    raw_metrics=metrics,
                    notes=f"Imported from {envelope.source_system}",
                    is_processed=True,
                )
            )
        else:
            raise ValueError(f"지원하지 않는 학습 이벤트 타입입니다: {envelope.event_type}")

        await session.flush()
        mark_success(event_log, "training_jobs", job.id)
    except Exception as exc:
        mark_failed(event_log, exc)

    await session.commit()
    await session.refresh(event_log)
    return event_log
