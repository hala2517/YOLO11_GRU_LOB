from datetime import datetime
from typing import Any, Literal

from app.models.enums import ExternalEventStatus
from pydantic import BaseModel, ConfigDict


class ExternalEventEnvelope(BaseModel):
    schema_version: str = "1.0"
    event_id: str
    source_system: str
    event_type: str
    occurred_at: datetime
    payload: dict[str, Any]


class ExternalEventLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_system: str
    event_id: str
    event_type: str
    schema_version: str
    occurred_at: datetime
    received_at: datetime
    payload: dict[str, Any]
    processed_status: ExternalEventStatus
    processed_at: datetime | None = None
    error_message: str | None = None
    retry_count: int
    related_entity_type: str | None = None
    related_entity_id: int | None = None


class StreamTokenRequest(BaseModel):
    camera_id: int
    stream_type: Literal["whep", "hls", "iframe"] | None = None


class StreamTokenResponse(BaseModel):
    camera_id: int
    token: str
    expires_at: datetime


class CameraStreamResponse(BaseModel):
    camera_id: int
    name: str
    stream_type: str
    playback_url: str
    path: str
    expires_at: datetime
    status: str
