import enum


class DeviceStatus(str, enum.Enum):
    online = "online"
    offline = "offline"
    error = "error"
    maintenance = "maintenance"


class AlertSeverity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class AlertType(str, enum.Enum):
    helmet_color = "helmet_color"
    unauthorized_person = "unauthorized_person"
    intrusion = "intrusion"
    custom = "custom"


class AppEnv(str, enum.Enum):
    development = "development"
    staging = "staging"
    production = "production"


class AIModelType(str, enum.Enum):
    detection = "detection"
    action_detection = "action_detection"
    action_classification = "action_classification"
    classification = "classification"
    segmentation = "segmentation"


class TrainingJobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class LabelingTaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class DataCollectionJobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class RecognitionType(str, enum.Enum):
    worker = "worker"
    helmet = "helmet"
    action = "action"
    intrusion = "intrusion"
    custom = "custom"


class ShiftType(str, enum.Enum):
    day = "day"
    evening = "evening"
    night = "night"


class MesSyncStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"


class CollectedVideoStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class ExternalEventStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"


class StreamSessionStatus(str, enum.Enum):
    starting = "starting"
    running = "running"
    stopped = "stopped"
    failed = "failed"


class CctvCommandStatus(str, enum.Enum):
    success = "success"
    failed = "failed"
