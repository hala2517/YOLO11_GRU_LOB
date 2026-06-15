export const queryKeys = {
  auth: {
    me: ['auth', 'me'] as const,
  },
  sites: {
    all: (params?: Record<string, unknown>) => ['sites', params] as const,
    detail: (id: number) => ['sites', id] as const,
  },
  nvrs: {
    all: (params?: Record<string, unknown>) => ['nvrs', params] as const,
    detail: (id: number) => ['nvrs', id] as const,
    bySite: (siteId: number) => ['nvrs', 'site', siteId] as const,
    cameras: (nvrId: number) => ['nvrs', nvrId, 'cameras'] as const,
  },
  cameras: {
    all: (params?: Record<string, unknown>) => ['cameras', params] as const,
    detail: (id: number) => ['cameras', id] as const,
  },
  alerts: {
    logs: (params?: Record<string, unknown>) => ['alert-logs', params] as const,
    logDetail: (id: number) => ['alert-logs', id] as const,
    thresholds: (params?: Record<string, unknown>) => ['alert-thresholds', params] as const,
    thresholdDetail: (id: number) => ['alert-thresholds', id] as const,
  },
  ai: {
    models: (params?: Record<string, unknown>) => ['ai-models', params] as const,
    modelDetail: (id: number) => ['ai-models', id] as const,
    jobs: (params?: Record<string, unknown>) => ['training-jobs', params] as const,
    jobDetail: (id: number) => ['training-jobs', id] as const,
    datasets: (params?: Record<string, unknown>) => ['datasets', params] as const,
    datasetDetail: (id: number) => ['datasets', id] as const,
    evaluation: (params?: Record<string, unknown>) => ['evaluation-results', params] as const,
    evaluationDetail: (id: number) => ['evaluation-results', id] as const,
  },
  roles: {
    all: ['roles'] as const,
  },
} as const
