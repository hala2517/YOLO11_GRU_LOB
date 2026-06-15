import type { TimestampFields } from './common'
import type { DeviceStatus } from './nvr'

export interface Camera extends TimestampFields {
  id: number
  nvr_id: number
  site_id: number
  name: string
  camera_code: string
  description: string | null
  rtsp_url: string | null
  channel_number: number | null
  status: DeviceStatus
  is_active: boolean
  is_deleted: boolean
}

export interface CameraCreate {
  nvr_id: number
  name: string
  camera_code: string
  description?: string
  rtsp_url?: string
  channel_number?: number
  is_active?: boolean
}

export interface CameraUpdate {
  name?: string
  description?: string
  rtsp_url?: string
  channel_number?: number
  is_active?: boolean
}
