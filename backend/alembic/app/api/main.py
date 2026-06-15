from app.api.routers.ai_models import router as ai_models_router
from app.api.routers.collected_videos import router as collected_videos_router
from app.api.routers.cctv import router as cctv_router
from app.api.routers.alerts import alert_logs_router, alert_thresholds_router
from app.api.routers.annotations import annotations_router, images_router
from app.api.routers.cameras import router as cameras_router
from app.api.routers.data_collection_jobs import router as data_collection_jobs_router
from app.api.routers.datasets import router as datasets_router
from app.api.routers.efficiency_metrics import router as efficiency_metrics_router
from app.api.routers.evaluation_results import router as evaluation_results_router
from app.api.routers.external_events import router as external_events_router
from app.api.routers.external_ai import router as external_ai_router
from app.api.routers.health import router as health_router
from app.api.routers.labeling_tasks import router as labeling_tasks_router
from app.api.routers.line_productivity import router as line_productivity_router
from app.api.routers.lob_eb_criteria import router as lob_eb_criteria_router
from app.api.routers.mes_sync_logs import router as mes_sync_logs_router
from app.api.routers.monitoring import router as monitoring_router
from app.api.routers.nvrs import router as nvrs_router
from app.api.routers.processes import router as processes_router
from app.api.routers.recognition_logs import router as recognition_logs_router
from app.api.routers.roles import router as roles_router
from app.api.routers.sites import router as sites_router
from app.api.routers.standard_process_charts import router as standard_process_charts_router
from app.api.routers.training_jobs import router as training_jobs_router
from app.api.routers.users import router as users_router
from app.api.routers.worker_detections import router as worker_detections_router
from app.api.routers.worker_flow import router as worker_flow_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(users_router)
api_router.include_router(sites_router)
api_router.include_router(standard_process_charts_router)
api_router.include_router(lob_eb_criteria_router)
api_router.include_router(line_productivity_router)
api_router.include_router(nvrs_router)
api_router.include_router(cameras_router)
api_router.include_router(cctv_router)
api_router.include_router(alert_thresholds_router)
api_router.include_router(alert_logs_router)
api_router.include_router(ai_models_router)
api_router.include_router(roles_router)
api_router.include_router(training_jobs_router)
api_router.include_router(datasets_router)
api_router.include_router(evaluation_results_router)
api_router.include_router(external_events_router)
api_router.include_router(external_ai_router)
api_router.include_router(labeling_tasks_router)
api_router.include_router(annotations_router)
api_router.include_router(images_router)
api_router.include_router(data_collection_jobs_router)
api_router.include_router(recognition_logs_router)
api_router.include_router(monitoring_router)
api_router.include_router(processes_router)
api_router.include_router(efficiency_metrics_router)
api_router.include_router(mes_sync_logs_router)
api_router.include_router(worker_detections_router)
api_router.include_router(worker_flow_router)
api_router.include_router(collected_videos_router)
