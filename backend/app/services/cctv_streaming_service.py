import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

from app.core.config import get_settings
from app.models.camera import Camera
from app.models.enums import StreamSessionStatus
from app.models.stream_session import StreamSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


def _stream_path(camera: Camera) -> str:
    return f"site-{camera.site_id}/camera-{camera.id}"


def _sign(data: bytes) -> str:
    settings = get_settings()
    digest = hmac.new(settings.secret_key.encode(), data, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


def create_stream_token(camera_id: int, stream_type: str | None = None) -> tuple[str, datetime]:
    settings = get_settings()
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=settings.stream_token_expire_seconds
    )
    payload = {
        "camera_id": camera_id,
        "stream_type": stream_type or settings.cctv_stream_mode,
        "exp": int(expires_at.timestamp()),
    }
    data = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode()
    token = f"{data}.{_sign(data.encode())}"
    return token, expires_at


def build_playback_url(camera: Camera, token: str, stream_type: str | None = None) -> tuple[str, str]:
    settings = get_settings()
    selected_type = stream_type or settings.cctv_stream_mode
    path = _stream_path(camera)

    if selected_type == "whep":
        base_url = settings.media_mtx_whep_base_url.rstrip("/")
        return f"{base_url}/{path}/whep?{urlencode({'token': token})}", path
    if selected_type == "hls":
        base_url = settings.hls_public_base_url.rstrip("/")
        return f"{base_url}/{path}/playlist.m3u8?{urlencode({'token': token})}", path

    return f"/api/v1/cameras/{camera.id}/iframe?{urlencode({'token': token})}", path


async def get_camera_or_none(session: AsyncSession, camera_id: int) -> Camera | None:
    result = await session.execute(
        select(Camera).where(Camera.id == camera_id, Camera.is_deleted.is_(False))
    )
    return result.scalar_one_or_none()


async def create_or_touch_stream_session(
    session: AsyncSession,
    camera: Camera,
    playback_url: str,
    path: str,
    stream_type: str,
) -> StreamSession:
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(StreamSession)
        .where(
            StreamSession.camera_id == camera.id,
            StreamSession.stream_type == stream_type,
            StreamSession.status == StreamSessionStatus.running,
        )
        .order_by(StreamSession.id.desc())
    )
    session_row = result.scalars().first()
    if session_row is None:
        session_row = StreamSession(
            camera_id=camera.id,
            stream_type=stream_type,
            path=path,
            playback_url=playback_url,
            status=StreamSessionStatus.running,
            started_at=now,
            last_accessed_at=now,
        )
        session.add(session_row)
    else:
        session_row.playback_url = playback_url
        session_row.path = path
        session_row.last_accessed_at = now

    await session.flush()
    return session_row
