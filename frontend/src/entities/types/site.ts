import type { TimestampFields } from './common'

export interface Site extends TimestampFields {
  id: number
  name: string
  code: string | null
  address: string | null
  description: string | null
  is_active: boolean
  is_deleted: boolean
}

export interface SiteCreate {
  name: string
  code?: string
  address?: string
  description?: string
  is_active?: boolean
}

export interface SiteUpdate {
  name?: string
  code?: string
  address?: string
  description?: string
  is_active?: boolean
}
