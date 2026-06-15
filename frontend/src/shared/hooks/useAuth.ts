import { clearToken, getToken, setToken } from '@/shared/api/client'

export function useAuth() {
  const token = getToken()

  return {
    isAuthenticated: !!token,
    token,
    login: (accessToken: string) => setToken(accessToken),
    logout: () => {
      clearToken()
      window.location.href = '/login'
    },
  }
}
