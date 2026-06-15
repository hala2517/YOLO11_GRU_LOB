import { cn } from '@/shared/lib/utils'

interface LoadingSpinnerProps {
  className?: string
  size?: 'sm' | 'md' | 'lg'
}

const sizeClass = { sm: 'h-4 w-4', md: 'h-6 w-6', lg: 'h-8 w-8' }

export function LoadingSpinner({ className, size = 'md' }: LoadingSpinnerProps) {
  return (
    <div
      role="status"
      aria-label="로딩 중"
      className={cn(
        'animate-spin rounded-full border-2 border-border border-t-primary',
        sizeClass[size],
        className,
      )}
    />
  )
}
