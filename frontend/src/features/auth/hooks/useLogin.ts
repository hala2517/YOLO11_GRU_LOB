import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { authApi } from '../api/authApi'
import { useAuth } from '@/shared/hooks/useAuth'
import type { LoginRequest } from '@/entities/types'

export function useLogin() {
  const navigate = useNavigate()
  const { login } = useAuth()

  return useMutation({
    mutationFn: (data: LoginRequest) => authApi.login(data),
    onSuccess: (data) => {
      login(data.access_token)
      navigate('/dashboard', { replace: true })
    },
  })
}
