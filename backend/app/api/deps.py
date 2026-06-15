from collections.abc import AsyncGenerator
from typing import Annotated

from app.core.security import decode_access_token
from app.db.session import async_session_factory
from app.models.user import User
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

bearer_scheme = HTTPBearer()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효하지 않은 인증 토큰입니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(credentials.credentials)
        login_id: str | None = payload.get("sub")
        if login_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await session.execute(
        select(User).where(User.login_id == login_id, User.is_deleted.is_(False))
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다.",
        )
    return user


def require_role(*role_names: str):
    """
    Role 기반 접근 제어 Dependency — 현재 미사용, 향후 확장 시 활성화.

    사용 예시:
        @router.get("/admin", dependencies=[Depends(require_role("admin"))])
        async def admin_endpoint(): ...
    """

    async def _checker(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        user_role_names = {r.name for r in getattr(current_user, "roles", [])}
        if not user_role_names.intersection(role_names):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="해당 작업을 수행할 권한이 없습니다.",
            )
        return current_user

    return _checker
