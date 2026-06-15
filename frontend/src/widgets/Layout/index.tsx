import { Sidebar } from '@/widgets/Sidebar'
import { Header } from '@/widgets/Header'
import { Outlet } from 'react-router-dom'

export function Layout() {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
