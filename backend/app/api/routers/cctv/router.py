from typing import Annotated

from app.api.deps import get_current_user, get_db_session
from app.models.user import User
from app.schemas.external_events import StreamTokenRequest, StreamTokenResponse
from app.services.cctv_streaming_service import create_stream_token, get_camera_or_none
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cctv", tags=["cctv"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/stream-token", response_model=StreamTokenResponse)
async def create_cctv_stream_token(
    body: StreamTokenRequest,
    session: DbSession,
    current_user: CurrentUser,
) -> StreamTokenResponse:
    camera = await get_camera_or_none(session, body.camera_id)
    if camera is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="카메라를 찾을 수 없습니다.",
        )

    token, expires_at = create_stream_token(camera.id, body.stream_type)
    return StreamTokenResponse(camera_id=camera.id, token=token, expires_at=expires_at)
