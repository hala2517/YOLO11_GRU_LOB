from app.schemas.nvr.base import NVRBase


class NVRCreate(NVRBase):
    password: str | None = None  # 평문 수신, 백엔드에서 암호화
