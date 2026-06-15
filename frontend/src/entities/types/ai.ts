import type { TimestampFields } from './common'

export type AIModelType =
  | 'detection'
  | 'action_detection'
  | 'action_classification'
  | 'classification'
  | 'segmentation'

export type TrainingJobStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'

export interface AIModel extends TimestampFields {
  id: number
  name: string
  version: string
  model_type: AIModelType
  description: string | null
  is_active: boolean
}

export interface Dataset extends TimestampFields {
  id: number
  name: string
  description: string | null
  total_images: number
  labeled_images: number
  is_active: boolean
  created_by: number | null
}

export interface DatasetCreate {
  name: string
  description?: string
  total_images?: number
  labeled_images?: number
  is_active?: boolean
  created_by?: number
}

export interface DatasetUpdate {
  name?: string
  description?: string
  total_images?: number
  labeled_images?: number
  is_active?: boolean
}

export interface TrainingJob extends TimestampFields {
  id: number
  job_name: string
  model_id: number | null
  dataset_id: number
  status: TrainingJobStatus
  parameters: Record<string, unknown> | null
  metrics: Record<string, unknown> | null
  created_by: number | null
  started_at: string | null
  completed_at: string | null
}

export interface TrainingJobCreate {
  job_name: string
  model_id?: number
  dataset_id: number
  parameters?: Record<string, unknown>
  created_by?: number
}

export interface EvaluationResult extends TimestampFields {
  id: number
  model_id: number
  dataset_id: number | null
  training_job_id: number | null
  evaluation_date: string
  mAP: number | null
  precision: number | null
  recall: number | null
  f1_score: number | null
  inference_time_ms: number | null
  accuracy: number | null
  source_file_path: string
  file_hash: string | null
  raw_metrics: Record<string, unknown>
  notes: string | null
  is_processed: boolean
}
