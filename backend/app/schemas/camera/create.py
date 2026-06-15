from app.schemas.camera.base import CameraBase


class CameraCreate(CameraBase):
    pass  # site_id는 nvr_id를 통해 백엔드에서 자동 채움
