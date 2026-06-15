import { apiClient } from '@/shared/api/client'
import type { LoginRequest, Token, User } from '@/entities/types'

export const authApi = {
  login: async (data: LoginRequest): Promise<Token> => {
    const res = await apiClient.post<Token>('/users/login', data)
    return res.data
  },

  getMe: async (): Promise<User> => {
    const res = await apiClient.get<User>('/users/me')
    return res.data
  },
}
