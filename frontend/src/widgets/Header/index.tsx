import { useAuth } from '@/shared/hooks/useAuth'
import { LogOut, Moon, Sun, User } from 'lucide-react'
import { useTheme } from '@/app/providers/ThemeProvider'

export function Header() {
  const { logout } = useAuth()
  const { theme, setTheme } = useTheme()

  return (
    <header className="flex h-14 items-center justify-end gap-2 border-b border-border bg-background px-4">
      <button
        onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        className="rounded-md p-2 hover:bg-accent hover:text-accent-foreground"
        title="테마 변경"
      >
        {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
      </button>

      <button
        className="rounded-md p-2 hover:bg-accent hover:text-accent-foreground"
        title="프로필"
      >
        <User size={16} />
      </button>

      <button
        onClick={logout}
        className="rounded-md p-2 hover:bg-accent hover:text-accent-foreground"
        title="로그아웃"
      >
        <LogOut size={16} />
      </button>
    </header>
  )
}
