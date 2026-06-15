export const sites = [
  { id: 1, name: 'Site A', area: '생산 1라인', status: 'online', workers: 28, alerts: 2 },
  { id: 2, name: 'Site B', area: '포장 구역', status: 'warning', workers: 17, alerts: 5 },
  { id: 3, name: 'Site C', area: '검사 구역', status: 'offline', workers: 8, alerts: 0 },
]

export const nvrs = [
  { id: 1, name: 'NVR-Main-01', ip: '192.168.10.21', port: 554, status: 'online', siteId: 1 },
  { id: 2, name: 'NVR-Pack-02', ip: '192.168.10.35', port: 554, status: 'warning', siteId: 2 },
  { id: 3, name: 'NVR-QA-03', ip: '192.168.10.44', port: 8554, status: 'offline', siteId: 3 },
]

export const cameras = [
  { id: 1, name: 'Camera-01', siteId: 1, nvrId: 1, zone: '입구', status: 'online', resolution: '1920x1080', fps: 30 },
  { id: 2, name: 'Camera-02', siteId: 1, nvrId: 1, zone: '생산 1라인', status: 'online', resolution: '1920x1080', fps: 30 },
  { id: 3, name: 'Camera-03', siteId: 2, nvrId: 2, zone: '포장 구역', status: 'warning', resolution: '1280x720', fps: 24 },
  { id: 4, name: 'Camera-04', siteId: 3, nvrId: 3, zone: '검사 구역', status: 'offline', resolution: '1920x1080', fps: 0 },
]

export const collectionJobs = [
  { id: 1, camera: 'Camera-01', status: 'running', schedule: '매일 08:00-18:00', progress: 64 },
  { id: 2, camera: 'Camera-02', status: 'completed', schedule: '수동 실행', progress: 100 },
  { id: 3, camera: 'Camera-03', status: 'failed', schedule: '매시간', progress: 18 },
]

export const collectedVideos = [
  { id: 1, camera: 'Camera-01', fileName: 'line1_20260506_0900.mp4', status: 'completed', duration: '00:12:30', size: '824MB' },
  { id: 2, camera: 'Camera-02', fileName: 'helmet_zone_0905.mp4', status: 'completed', duration: '00:08:44', size: '512MB' },
  { id: 3, camera: 'Camera-03', fileName: 'packing_0910.mp4', status: 'processing', duration: '00:04:10', size: '210MB' },
]

export const datasets = [
  { id: 1, name: '안전모 검출 v1', images: 1240, labels: 3180, quality: 96, status: 'ready' },
  { id: 2, name: '작업자 동선 v2', images: 860, labels: 1420, quality: 91, status: 'review' },
  { id: 3, name: 'AMR 위험구역 v1', images: 540, labels: 980, quality: 88, status: 'draft' },
]

export const labelingTasks = [
  { id: 1, name: 'Helmet bbox #12', dataset: '안전모 검출 v1', status: 'running', progress: 72 },
  { id: 2, name: 'Worker flow #04', dataset: '작업자 동선 v2', status: 'pending', progress: 35 },
  { id: 3, name: 'AMR zone #02', dataset: 'AMR 위험구역 v1', status: 'completed', progress: 100 },
]

export const annotations = [
  { id: 1, className: 'worker', box: 'x:120 y:84 w:180 h:260', confidence: 0.98 },
  { id: 2, className: 'helmet', box: 'x:148 y:52 w:72 h:58', confidence: 0.94 },
  { id: 3, className: 'amr', box: 'x:410 y:230 w:160 h:120', confidence: 0.91 },
]

export const trainingJobs = [
  { id: 1, name: 'YOLO Helmet Train', dataset: '안전모 검출 v1', status: 'running', progress: 68, map: 0.82 },
  { id: 2, name: 'Worker Action Model', dataset: '작업자 동선 v2', status: 'completed', progress: 100, map: 0.88 },
  { id: 3, name: 'AMR Intrusion Model', dataset: 'AMR 위험구역 v1', status: 'failed', progress: 41, map: 0.51 },
]

export const evaluationResults = [
  { id: 1, model: 'helmet-detector-v1', accuracy: 94, precision: 92, recall: 89, map: 86 },
  { id: 2, model: 'worker-flow-v2', accuracy: 91, precision: 88, recall: 90, map: 84 },
  { id: 3, model: 'amr-zone-v1', accuracy: 87, precision: 84, recall: 82, map: 79 },
]

export const alertThresholds = [
  { id: 1, name: '출입구 비인가자', site: 'Site A', camera: 'Camera-01', severity: 'critical', active: 'ON' },
  { id: 2, name: '포장구역 침입', site: 'Site B', camera: 'Camera-03', severity: 'high', active: 'ON' },
]

export const alertLogs = [
  { id: 1, title: '비인가자 접근 감지', site: 'Site A', camera: 'Camera-01', severity: 'critical', acknowledged: false, time: '09:12:22' },
  { id: 2, title: '작업자 안전모 미착용', site: 'Site A', camera: 'Camera-02', severity: 'high', acknowledged: false, time: '09:18:04' },
  { id: 3, title: 'AMR 위험구역 접근', site: 'Site B', camera: 'Camera-03', severity: 'medium', acknowledged: true, time: '09:21:40' },
]

export const recognitionLogs = [
  { id: 1, camera: 'Camera-01', type: 'worker', message: '작업자 3명 감지', time: '09:20:11' },
  { id: 2, camera: 'Camera-02', type: 'helmet', message: '안전모 착용 92%', time: '09:21:05' },
  { id: 3, camera: 'Camera-03', type: 'amr', message: 'AMR 1대 이동 중', time: '09:22:33' },
]

export const workerDetections = [
  { id: 1, worker: 'W-102', process: '투입', duration: '12m', status: 'normal' },
  { id: 2, worker: 'W-118', process: '조립', duration: '28m', status: 'delay' },
  { id: 3, worker: 'W-141', process: '검사', duration: '9m', status: 'normal' },
]

export const processes = [
  { id: 1, name: '투입', output: 320, tact: 42, workers: 5 },
  { id: 2, name: '조립', output: 288, tact: 55, workers: 12 },
  { id: 3, name: '검사', output: 276, tact: 48, workers: 6 },
  { id: 4, name: '포장', output: 260, tact: 52, workers: 5 },
]

export const efficiencyMetrics = [
  { name: '08시', production: 42, tact: 56, efficiency: 84 },
  { name: '09시', production: 58, tact: 48, efficiency: 91 },
  { name: '10시', production: 51, tact: 52, efficiency: 88 },
  { name: '11시', production: 64, tact: 44, efficiency: 95 },
]

export const mesSyncLogs = [
  { id: 1, lot: 'LOT-20260506-A1', status: 'success', process: '조립', records: 124, time: '09:00:11' },
  { id: 2, lot: 'LOT-20260506-B2', status: 'processing', process: '검사', records: 88, time: '09:13:42' },
  { id: 3, lot: 'LOT-20260506-C3', status: 'failed', process: '포장', records: 36, time: '09:24:07' },
]

export const trendData = [
  { name: '08:00', worker: 12, helmet: 18, alert: 2 },
  { name: '09:00', worker: 18, helmet: 24, alert: 5 },
  { name: '10:00', worker: 22, helmet: 28, alert: 3 },
  { name: '11:00', worker: 19, helmet: 26, alert: 1 },
]
