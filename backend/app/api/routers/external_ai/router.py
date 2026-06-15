from typing import Annotated

from app.api.deps import get_db_session
from app.schemas.external_events import ExternalEventEnvelope, ExternalEventLogResponse
from app.services.ai_inference_event_service import process_recognition_event
from app.services.ai_training_event_service import process_training_event
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/external/ai", tags=["external-ai"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.post("/training-events", response_model=ExternalEventLogResponse)
async def receive_training_event(
    body: ExternalEventEnvelope,
    session: DbSession,
) -> ExternalEventLogResponse:
    event_log = await process_training_event(session, body)
    return ExternalEventLogResponse.model_validate(event_log)


@router.post("/recognition-events", response_model=ExternalEventLogResponse)
async def receive_recognition_event(
    body: ExternalEventEnvelope,
    session: DbSession,
) -> ExternalEventLogResponse:
    event_log = await process_recognition_event(session, body)
    return ExternalEventLogResponse.model_validate(event_log)
