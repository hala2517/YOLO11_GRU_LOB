import type { TimestampFields } from './common'

export interface User extends TimestampFields {
  id: number
  login_id: string
  email: string | null
  name: string
  is_active: boolean
  is_deleted: boolean
  last_login_at: string | null
  password_changed_at: string | null
}

export interface Token {
  access_token: string
  token_type?: string
}

export interface LoginRequest {
  login_id: string
  password: string
}

export interface RegisterRequest {
  login_id: string
  password: string
  name: string
}
