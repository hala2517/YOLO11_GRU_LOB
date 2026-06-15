from pydantic import BaseModel


class DatasetUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    total_images: int | None = None
    labeled_images: int | None = None
    storage_path: str | None = None
    version: str | None = None
    is_active: bool | None = None
