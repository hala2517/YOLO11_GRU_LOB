import { getToken } from '@/shared/api/client'
import { Navigate, Outlet } from 'react-router-dom'

export function ProtectedRoute() {
  const token = getToken()

  if (!token) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}
