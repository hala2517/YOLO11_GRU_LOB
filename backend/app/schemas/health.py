from pydantic import BaseModel, ConfigDict


class HealthCheck(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str
    environment: str
    app_name: str
    version: str
