import type { TimestampFields } from './common'

export type DeviceStatus = 'online' | 'offline' | 'error' | 'maintenance'

export interface NVR extends TimestampFields {
  id: number
  site_id: number
  name: string
  description: string | null
  ip_address: string
  port: number
  username: string | null
  model_name: string | null
  firmware_version: string | null
  storage_capacity_gb: number | null
  status: DeviceStatus
  is_active: boolean
  is_deleted: boolean
}

export interface NVRCreate {
  site_id: number
  name: string
  description?: string
  ip_address: string
  port?: number
  username?: string
  password?: string
  model_name?: string
  firmware_version?: string
  storage_capacity_gb?: number
  is_active?: boolean
}

export interface NVRUpdate {
  name?: string
  description?: string
  ip_address?: string
  port?: number
  username?: string
  password?: string
  model_name?: string
  firmware_version?: string
  storage_capacity_gb?: number
  is_active?: boolean
}
