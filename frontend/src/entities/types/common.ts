export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
}

export interface ApiError {
  detail: string
}

export interface TimestampFields {
  created_at: string
  updated_at: string
}
