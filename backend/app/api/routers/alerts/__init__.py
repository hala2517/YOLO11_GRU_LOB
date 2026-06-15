from app.api.routers.alerts.alert_logs import router as alert_logs_router
from app.api.routers.alerts.alert_thresholds import router as alert_thresholds_router

__all__ = ["alert_thresholds_router", "alert_logs_router"]
