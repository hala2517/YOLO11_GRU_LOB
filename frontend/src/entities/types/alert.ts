import type { TimestampFields } from './common'

export type AlertSeverity = 'low' | 'medium' | 'high' | 'critical'
export type AlertType =
  | 'amr_collision'
  | 'helmet_color'
  | 'unauthorized_person'
  | 'intrusion'
  | 'custom'

export interface AlertThreshold extends TimestampFields {
  id: number
  site_id: number
  name: string
  alert_type: AlertType
  threshold_value: number | null
  description: string | null
  is_active: boolean
  created_by: number | null
}

export interface AlertThresholdCreate {
  site_id: number
  name: string
  alert_type: AlertType
  threshold_value?: number
  description?: string
  is_active?: boolean
  created_by?: number
}

export interface AlertThresholdUpdate {
  name?: string
  alert_type?: AlertType
  threshold_value?: number
  description?: string
  is_active?: boolean
}

export interface AlertLog extends TimestampFields {
  id: number
  camera_id: number | null
  threshold_id: number | null
  site_id: number | null
  alert_type: AlertType
  severity: AlertSeverity
  message: string | null
  snapshot_path: string | null
  is_acknowledged: boolean
  acknowledged_by: number | null
  acknowledged_at: string | null
}
