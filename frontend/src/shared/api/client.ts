import axios from 'axios'
import { toast } from 'sonner'

const TOKEN_KEY = 'aipoc_token'

export const getToken = (): string | null => localStorage.getItem(TOKEN_KEY)
export const setToken = (token: string): void => localStorage.setItem(TOKEN_KEY, token)
export const clearToken = (): void => localStorage.removeItem(TOKEN_KEY)

export const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

apiClient.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearToken()
      window.location.href = '/login'
      return Promise.reject(error)
    }

    const message: string =
      error.response?.data?.detail ?? error.message ?? '알 수 없는 오류가 발생했습니다.'

    toast.error(message)
    return Promise.reject(error)
  },
)
