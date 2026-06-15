from pydantic import BaseModel


class AlertLogAcknowledge(BaseModel):
    acknowledged_by: int | None = None
